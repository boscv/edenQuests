package edenQuests;

use strict;
use warnings;
use Plugins;
use Log qw(message warning error);
use Commands;
use Settings;
use File::Spec;
use File::Basename qw(dirname);
use Cwd qw(getcwd abs_path);
use Encode qw(decode);
use Globals qw($char);

Plugins::register('edenQuests', 'Quests do Grupo Éden', \&onUnload);

my $plugin_dir  = dirname(abs_path(__FILE__));
my $supabase_url = "https://bnjjwtbjanjkledoiwem.supabase.co";
my $anon_key     = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJuamp3dGJqYW5qa2xlZG9pd2VtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAxOTk4MzAsImV4cCI6MjA3NTc3NTgzMH0.N3wNjGbKM8QCZ2v3EbXksgawmwdG5Vo1AxQUE_81K10"; # ajuste se necessário
my $python_cmd   = "python3";
my $injection_done;
my $injection_in_progress;
my $auth_status       = 'unknown';
my $in_game_hook;

register_hooks();
maybe_inject_macros();

sub maybe_inject_macros {
    return if $injection_done || $injection_in_progress;
    return unless $char && $char->{charID};

    my ($macro_file, $macro_display) = resolve_macro_destination();

    unless (-e $macro_file) {
        warning "[edenQuests] Arquivo $macro_file não encontrado. Abortando.\n";
        return;
    }

    $injection_in_progress = 1;

    message "[edenQuests] Preparando $macro_display para injeção...\n";

    if (update_proxy_and_inject($macro_file)) {
        $injection_done = 1;
        $auth_status    = 'allowed';
    }

    $injection_in_progress = 0;
}

sub resolve_macro_destination {
    my $control_dir;

    if (my $config_path = eval { Settings::getControlFilename("config.txt") }) {
        $control_dir = dirname($config_path) if $config_path;
    }

    unless ($control_dir) {
        $control_dir = File::Spec->catdir(getcwd(), "control");
    }

    my $macro_file = File::Spec->catfile($control_dir, "eventMacros.txt");
    my $macro_display = eval { File::Spec->abs2rel($macro_file, getcwd()) } || $macro_file;

    return ($macro_file, $macro_display);
}

sub update_proxy_and_inject {
    my ($macro_file) = @_;
    my ($res, $decoded) = fetch_macro_payload();

    return 0 if $res != 0;

    if ($decoded !~ /automacro|timeout|call\s*\{/) {
        warning "[edenQuests] Não parece um eventMacro — abortando. Prévia: "
            . substr($decoded,0,200) . "\n";
        return 0;
    }

    unless (-e $macro_file) {
        warning "[edenQuests] Arquivo $macro_file não encontrado. Abortando.\n";
        return 0;
    }

    my $original = "";
    if (open my $mf, "<", $macro_file) { local $/; $original = <$mf>; close $mf; }

    if (open my $out, ">", $macro_file) {
        print $out $original;
        print $out "\n\n# --- [edenQuests] NÃO DELETE ---\n";
        print $out $decoded;
        close $out;
    } else {
        warning "[edenQuests] Falha ao escrever $macro_file\n";
        return 0;
    }

    Commands::run("reload eventMacros");

    if (open my $rf, ">", $macro_file) {
        print $rf $original;
        close $rf;
    } else {
        warning "[edenQuests] Falha ao restaurar $macro_file\n";
    }

    return 1;
}

sub register_hooks {
    unregister_hooks();
    $in_game_hook = Plugins::addHook('in_game', \&maybe_inject_macros);
}

sub unregister_hooks {
    if ($in_game_hook) {
        Plugins::delHook($in_game_hook);
        undef $in_game_hook;
    }
}

sub onUnload {
	Commands::run("reload eventMacros");
    unregister_hooks();

    $injection_done        = 0;
    $injection_in_progress = 0;
    $auth_status           = 'unknown';

    message "[edenQuests] Plugin descarregado.\n";
}

sub fetch_macro_payload {
    my ($quiet) = @_;
    my $py_script = File::Spec->catfile($plugin_dir, "proxy.py");
    my $cmd = qq("$python_cmd" "$py_script" "$supabase_url" "$anon_key");

    message "[edenQuests] Executando (stdout) ...\n" unless $quiet;

    my $output = `$cmd 2>&1`;
    my $res = $? >> 8;

    $output = eval { decode("UTF-8", $output) } || $output;

    if ($res != 0) {
        unless ($quiet) {
            warning "[edenQuests] Acesso negado. stderr:\n$output\n";
            if ($output =~ /hash_mismatch/i) {
                warning "[edenQuests] Atualize o plugin:\n";
                warning "[GitHub] https://github.com/billabong93/edenQuests\n";
            } else {
                warning "[edenQuests] Verifique sua licença com o suporte:\n";
                warning "[Discord] https://discord.com/users/boscv. \n";
            }
        }
        return ($res, undef);
    }

    return (0, $output);
}

1;