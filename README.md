## ⚜️ edenQuests v2.5 (LATAM)
[<img alt="Static Badge" src="https://img.shields.io/badge/GitHub-Openkore-%0FBF3E?logo=discord&logoColor=%23fff">](https://github.com/OpenKore/openkore)\
[<img alt="Static Badge" src="https://img.shields.io/badge/GitHub-GordoKore-%0FBF3E?logo=discord&logoColor=%23fff">](https://github.com/Brunnexo/GordoKore)\
[<img alt="Static Badge" target="_blank" src="https://img.shields.io/badge/Discord-boscv.-%237289DA?logo=discord&logoColor=%23fff">](https://discord.com/users/boscv.)\
[<img alt="Static Badge" src="https://img.shields.io/badge/Discord-Openkore%20LATAM-%237289DA?logo=discord&logoColor=%23fff">](https://discord.gg/SNJ4qGn8)

Plugin de injeção de eventMacros para Quests e Equipamentos do Éden - Openkore (ROla)

---

### 📚 Sumário
- [📜 Quests Incluídas](#-quests-inclu%C3%ADdas)
- [🤖 Funções Principais](#-fun%C3%A7%C3%B5es-principais)
- [⚙️ Requisitos](#%EF%B8%8F-requisitos)
- [📝 Instruções](#-instru%C3%A7%C3%B5es)
- [🛠️ Configurações necessárias](#%EF%B8%8F-configura%C3%A7%C3%B5es-necess%C3%A1rias)
- [⚠️ O que não fazer](#%EF%B8%8F-o-que-n%C3%A3o-fazer)
- [📢 Informações e avisos](#-informa%C3%A7%C3%B5es-e-avisos)
- [🗃️ Estrutura da pasta](#%EF%B8%8F-estrutura-da-pasta)
- [🚀 Implementações futuras](#-implementa%C3%A7%C3%B5es-futuras)
- [🤝 Apoie o projeto](#-apoie-o-projeto)

 
---

### 📜 Quests Incluídas

  - **Resgate de equipamentos** dos níveis 7 ao 160.
  - **Quests da Instrutora Boya** dos níveis 26, 33, 40 e 75.
  - **Quests do Instrutor Ur** dos níveis 60, 70, 80 e 90.
  - **Quests do Éden** dos níveis 100+.
  - **Quests Primeiros Passos** para Aprendiz.
  - **Quests Tutoriais** para Aprendiz (Apenas as que dão consumíveis).
  - **Quest do Novo Mundo** da Agência Pata de Gato.
  - **Quests de Renascimento**, pagando ou capturando o Livro Fugitivo.
  - **1ª Mudança de Classe** para as classes principais.
  - **2ª Mudança de Classe à Transclasse** para Lorde, Mestre e Desordeiro.

---

### 🤖 Funções Principais:

  - **Mudança de classe** para 1ª classe, e 2ª classe à transclasse.
  - **Rotas de UP** para agilizar e facilitar seu trabalho.
  - **Configuração personalizada** de equipamentos, encantamentos e cartas.
  - **Escolha o nível** em que quer que o personagem inicie as quests (26-90).
  - **Equipa automáticamente** itens recebidos após as quests.
  - **Teleport Search** (*teleportAuto_search*) para maior eficiência e sobrevivência.
  - **Compra automática** e uso de Asas de Mosquito e Poções Laranjas. (26-90) (Possível desativar)
  - **Salva na Kafra** mais próxima da quest, para retorno mais rápido em caso de morte ou compra.
  - **Retorno seguro** ao local original do bot, restaurando configurações.
  - **Failsafes** para concluir quests. Seu personagem vai sempre continuar de onde parou.
  - **Compatível com profiles** pra você que gosta de manter as coisas organizadas.

---

## ⚙️ Requisitos:

  - Python
  - [Plugin eventMacros](https://github.com/OpenKore/openkore/tree/master/plugins/eventMacro) atualizado. 
  - [Plugin mapNormalizer](https://github.com/boscv/openkore/blob/master/plugins/mapNormalizer/mapNormalizer.pl) ativado no **sys.txt**
  - Se não existir, criar um arquivo **eventMacros.txt** na pasta **./control.**
  - [./fields](https://github.com/boscv/openkore/tree/master/fields/ROla) e [portals.txt](https://github.com/OpenKore/openkore/blob/master/tables/ROla/portals.txt) atualizados.

---

### 📝 Instruções:

  - Use **config.py** para configurar suas opções de quests, níveis, equipamentos, encantamentos, cartas e consumíveis.
    Nele, há explicações sobre cada configuração e suas respectivas funções.
  - Adicione *edenQuests* em **sys.txt** no final da linha *loadPlugins_list*.
  - Em caso de necessidade de reinjeção, use *'plugin reload edenQuests'* no console.
  - O HWID é gerado após o personagem estar online.

---

### 🛠️ Configurações necessárias:

* **config.txt**:
  - *statsAddAuto* *skillsAddAuto* definidos para o personagem upar atributos/skills.
  - *storageAuto_npc* com coordenadas configuradas (se não estiver usando as rotas).
  - *route_maxWarpFee* vazio ou com valor acima de 20000.

* **routeweights.txt**:
  - *AIRSHIP* 500
  - *moc_fild20* 10000

---

### ⚠️ O que não fazer:

  - *'reload eventMacros'*, *'reload all'* durante a execução do plugin.
  - **Jamais apague as variáveis** criadas pelo/para o plugin em **config.txt**, salvo necessidade
    de rollback por falha na execução de etapas do macro, ou a remoção do plugin.
  - **Não faça alterações** no **proxy.py** ou **edenQuests.pl**. O acesso é barrado pelo servidor
    em caso de qualquer modificação ou ausência dos arquivos.

---

### 📢 Informações e avisos:

  - O **eventMacros.txt** injetado é atualizado diariamente, qualquer bug ou erro, favor informar.
  - No caso das classes principais, a quest de nível 60 só é feita após mudança para  2ª classe. A quest até pode ser feita pelas 1ªs classes principais, mas não receberão equipamentos após a conclusão até a mudança para 2ª classe.
  - A maior parte das classes foi testada, e as armas estão em sua maioria, se não todas,
    nas posições corretas. (Opções extraídas de .csv)
  - Telesearch é fundamental para a conclusão dessas quests, não é possível desativá-lo.
  - Se seu bot não está pegando o aeroplano ou usando os teleportes, verifique routeweights.txt,
    e *route_maxWarpFee* em **config.txt**.
  - As Asas de Mosquito só devem ser desabilitadas se houver algum outro item equivalente
    em *teleportAuto_item1*.
  - Apesar de interceptado, o bot continuará usando qualquer skill ou item configurado no
    seu **config.txt**, **macros.txt** e **eventMacros.txt**.
  - O plugin depende do seu *storageAuto_npc* configurado, configure um, caso não use a opção de rotas.
  - A injeção não sobrescreverá seu **eventMacros.txt**. De qualquer forma, sempre bom manter um backup.
  - O plugin não é configurado pra comprar ou fazer uso de pots de sp. Mas pegará do armazém ou
    comprará mais antes de começar qualquer quest, e usará, se seu bot estiver configurado para isso.

---

### 🗃️ Estrutura da pasta:

- openkore-master/
  * 📁 control/
    * 📄 eventMacros.txt
    * 📄 sys.txt
  * 📁 fields/
  * 📁 plugins/
    * 📁 edenQuests/
      * 📄 README.md
      * 📄 atualizador-edenQuests.bat
      * 📄 atualizador-edenQuests.ps1
      * 📄 config.py
      * 📄 edenQuests.pl
      * 📄 proxy.py
    * 📁 mapNormalizer
      * 📄 mapNormalizer.pl
  * 📁 tables/
    * 📁 ROla/
      * 📄 portals.txt

---

### 🚀 Implementações futuras

* Quests do Éden faltantes dos níveis 12, 20 e 50.
* Quests diárias 120+.
* Mais quests de mudança de classe.

---

### 🤝 Apoie o projeto
* O edenEquips é gratuito e continuará gratuito.
* Se ele te ajudou e você quiser contribuir, pode apoiar via Pix:
<img src=https://i.postimg.cc/DzNhY2JN/support.png width="200" height="200">
[4717fdb1-345a-4d5a-aab5-067f7ef8789a]


