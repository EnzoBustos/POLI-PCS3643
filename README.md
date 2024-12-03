# POLI-PCS3643
Esse repositório tem como objetivo guardar os Exercícios Programas (EP's) e materiais autorais criados para auxiliar na disciplina PCS3643 - Laboratório de Engenharia de Software 

Para acessar o site com servidor local basta executar python app.py dentro da pasta backend.

Segue a Documentação do projeto:

Introdução
O AedesWiki é uma plataforma colaborativa destinada a fornecer informações abrangentes sobre o mosquito Aedes aegypti, doenças relacionadas, métodos de prevenção e controle. O objetivo é conscientizar a população e promover ações para combater a proliferação desse vetor de doenças como dengue, zika e chikungunya.
A plataforma permite que usuários registrados criem artigos informativos, façam denúncias sobre possíveis focos do mosquito em suas comunidades e comentem notícias relacionadas. Os administradores têm a função de moderar o conteúdo, aprovar ou rejeitar artigos submetidos pelos usuários, gerenciar usuários e acompanhar denúncias realizadas.

Funcionalidades Principais
Usuários
Registro e Login: Usuários podem se registrar na plataforma fornecendo nome de usuário, e-mail e senha. Após o registro, podem fazer login para acessar funcionalidades exclusivas.
Criação de Artigos: Usuários logados podem criar artigos sobre tópicos relacionados ao Aedes aegypti. Os artigos submetidos ficam pendentes de aprovação por um administrador.
Denúncias: Qualquer usuário pode preencher um formulário de denúncia informando possíveis focos do mosquito em sua comunidade. É possível fornecer detalhes como localização, severidade e descrição da situação.
Comentários em Notícias: Usuários logados podem comentar em notícias recentes relacionadas ao mosquito e às doenças que transmite.
Visualização de Perfil: Usuários podem visualizar e editar suas informações de perfil, bem como acompanhar seus artigos submetidos e denúncias realizadas.
Administradores
Aprovação/Rejeição de Artigos: Administradores podem visualizar artigos pendentes e decidir aprová-los ou rejeitá-los. Artigos aprovados são publicados na wiki.
Gerenciamento de Usuários: Administradores podem visualizar a lista de usuários, excluir usuários indesejados e promover usuários a administradores.
Visualização e Resolução de Denúncias: Administradores têm acesso a todas as denúncias realizadas pelos usuários e podem marcar denúncias como resolvidas após a devida ação.

Estrutura do Site
Páginas Públicas
Página Inicial (/): Apresenta uma visão geral do site, informações sobre o mosquito e links para as principais funcionalidades.
Wiki (/wiki): Disponibiliza artigos aprovados sobre o Aedes aegypti e temas relacionados. Visitantes podem pesquisar artigos por meio de um campo de busca.
Notícias sobre Dengue (/dengue_news): Exibe notícias recentes sobre dengue, zika e chikungunya, obtidas de uma API externa. Usuários logados podem comentar nas notícias.
Formulário de Denúncia (/complaint_form): Permite que usuários relatem possíveis focos do mosquito.
Páginas para Usuários Logados
Criar Artigo (/create_article): Formulário para criação de novos artigos.
Meu Perfil (/profile): Exibe informações do usuário logado e links para funcionalidades adicionais.
Editar Perfil (/edit_profile): Permite que o usuário edite suas informações pessoais.
Meus Artigos (/my_articles): Lista os artigos submetidos pelo usuário, com opções para editar ou excluir.
Minhas Denúncias (/my_complaints): Exibe as denúncias realizadas pelo usuário.
Páginas de Administração
Gerenciar Artigos (/admin_manage_articles): Lista todos os artigos submetidos, permitindo que o administrador edite ou exclua qualquer artigo.
Aprovar Artigos (/admin/articles): Lista artigos pendentes de aprovação, com opções para aprovar ou rejeitar.
Gerenciar Usuários (/manage_users): Lista todos os usuários registrados, com opções para excluir ou promover a administrador.
Denúncias Pendentes (/admin/complaints): Exibe denúncias realizadas pelos usuários, com opção para marcar como resolvidas.

Fluxos de Usuário
Registro e Login
Registro:


Acesse a página de registro (/register).
Preencha o formulário com nome de usuário, e-mail e senha.
Submeta o formulário para criar uma conta.
Uma mensagem confirma o sucesso do registro e orienta a fazer login.
Login:


Acesse a página de login (/login).
Insira seu e-mail e senha cadastrados.
Após o login, o usuário é redirecionado para a página inicial ou para a página que tentou acessar anteriormente.
Criação de Artigos
Faça login na plataforma.
Navegue até a página de criação de artigos (/create_article).
Preencha o título e o conteúdo do artigo.
Submeta o artigo. Uma mensagem confirma o envio e informa que o artigo aguarda aprovação.
Denúncias
Acesse o formulário de denúncia (/complaint_form).
Preencha as informações solicitadas:
Nome
E-mail
Telefone
Local da denúncia
Severidade da situação
Método de combate desrespeitado
Mensagem descritiva (opcional)
Submeta o formulário. Uma mensagem confirma o envio da denúncia.
Comentários em Notícias
Faça login na plataforma.
Acesse a página de notícias (/dengue_news).
Escolha uma notícia e visualize os detalhes.
Utilize o formulário de comentários abaixo da notícia para adicionar um comentário.
Submeta o comentário. Ele será exibido abaixo da notícia juntamente com outros comentários.

Fluxos de Administrador
Aprovação de Artigos
Faça login com uma conta de administrador.
Acesse a página de aprovação de artigos (/admin/articles).
Visualize a lista de artigos pendentes.
Para cada artigo, é possível:
Ler o conteúdo completo.
Aprovar o artigo, tornando-o público na wiki.
Rejeitar o artigo, mudando seu status para "Rejeitado".
Gerenciamento de Usuários
Acesse a página de gerenciamento de usuários (/manage_users).
Visualize a lista de usuários com suas informações (nome, e-mail, tipo de usuário).
Para cada usuário, é possível:
Excluir o usuário da plataforma.
Promover o usuário a administrador.
Visualização e Resolução de Denúncias
Acesse a página de denúncias pendentes (/admin/complaints).
Visualize a lista de denúncias com detalhes fornecidos pelos usuários.
Para cada denúncia, é possível:
Marcar como resolvida, indicando que a ação necessária foi tomada.

Configuração e Implantação
Requisitos
Python 3.x
Flask e dependências listadas no código
Banco de dados PostgreSQL
Ambiente virtual (recomendado)
Instalação
Clone o repositório:

 git clone https://github.com/seu-usuario/aedeswiki.git
cd aedeswiki


Crie um ambiente virtual (opcional, mas recomendado):

 python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows


Instale as dependências:

 pip install -r requirements.txt


Configuração do Banco de Dados:

 Certifique-se de que o PostgreSQL está instalado e em execução. Configure as credenciais de acesso no código, especificamente na função connect_db().


Configuração do Banco de Dados
Crie o banco de dados:


Use o comando createdb db_grupo01 ou através de uma interface gráfica.
Certifique-se de que o usuário u_grupo01 com senha grupo01 tem acesso ao banco.
Crie as tabelas necessárias:


Execute os scripts SQL para criar as tabelas (users, articles, news, complaints, etc.).
Defina as colunas conforme usadas no código (veja as consultas SQL para referência).
Popule tabelas com dados iniciais (opcional):


Insira categorias padrão ou usuários administradores iniciais.
Executando o Aplicativo
Inicie o servidor Flask:

 
Execute python app.py dentro da pasta Backend
Acesse o site:


Abra o navegador e vá para http://localhost:5000.

Estrutura do Código
Principais Módulos
app.py: Arquivo principal que contém as rotas, modelos e lógica do aplicativo.
Templates: Localizados na pasta templates, contém os arquivos HTML renderizados pelas rotas.
Estáticos: Arquivos CSS, JavaScript e imagens estão na pasta static ou assets.
Descrição de Alguns Módulos e Funções
Conexão com o Banco de Dados:

 def connect_db():
    return psycopg2.connect(
        host="200.144.245.12",
        port="65432",
        database="db_grupo01",
        user="u_grupo01",
        password="grupo01"
    )


Modelos de Usuário:


Classe User que herda de UserMixin para integração com Flask-Login.
Método delete_user_by_id para excluir usuários.
Formulários:


LoginForm e RegisterForm utilizam Flask-WTF para validação de formulários.
Rotas de Autenticação:


/login: Lida com login de usuários.
/register: Permite o registro de novos usuários.
/logout: Faz logout do usuário atual.
Rotas para Funcionalidades do Usuário:


/create_article: Permite que usuários criem artigos.
/complaint_form: Formulário para denúncias.
/dengue_news: Exibe notícias e permite comentários.
/profile: Exibe o perfil do usuário.
/edit_profile: Permite editar informações de perfil.
/my_articles: Lista artigos do usuário.
/my_complaints: Lista de denúncias feitas pelo usuário.
Rotas de Administração:


/admin/articles: Lista artigos pendentes para aprovação.
/manage_users: Permite gerenciar usuários.
/admin/complaints: Exibe denúncias para resolução.
/admin_manage_articles: Permite que o administrador gerencie todos os artigos.
Templates
Estrutura:


Os templates utilizam o Jinja2 para renderização dinâmica.
Arquivos HTML organizados para cada funcionalidade (e.g., login.html, register.html, profile.html).
Templates Importantes:


index.html: Página inicial.
wiki.html: Exibe a wiki com artigos aprovados.
create_article.html: Formulário para criação de artigos.
admin_articles.html: Interface para administradores aprovarem artigos.
manage_users.html: Gerenciamento de usuários.
Banco de Dados
Tabelas Principais:


users: Armazena informações dos usuários (id, e-mail, nome de usuário, senha, tipo de usuário).
articles: Contém os artigos criados pelos usuários (id, título, conteúdo, status de aprovação).
complaints: Registra denúncias feitas pelos usuários.
news: Armazena notícias obtidas da API externa.
Campos Comuns:


created_at e updated_at para controle de registro.
Chaves estrangeiras para relacionar usuários a artigos e denúncias.

Considerações Técnicas
Segurança:


Senhas são armazenadas com hash utilizando werkzeug.security.
Rotas protegidas utilizam @login_required para garantir acesso apenas a usuários autenticados.
A chave secreta app.secret_key deve ser segura em produção.
Manejo de Sessões:


O Flask-Login é utilizado para gerenciar sessões de usuário.
Integração com API Externa:


A rota /dengue_news utiliza a API do NewsAPI para buscar notícias sobre a dengue.
As notícias são armazenadas no banco de dados para exibição e comentários.
Comentários em Notícias:


Os comentários são associados a notícias específicas e ao usuário que comentou.
Aprovação de Conteúdo:


Artigos submetidos pelos usuários têm um campo is_approved que indica se estão aprovados, pendentes ou rejeitados.
Apenas artigos aprovados são exibidos na wiki pública.
Roles de Usuário:


O campo user_type distingue entre usuários normais e administradores.
Funcionalidades administrativas são protegidas para acesso apenas por administradores.

Contato e Suporte
Em caso de dúvidas, sugestões ou problemas, entre em contato com a equipe responsável:
E-mail: aedeswiki@exemplo.gov
Telefone: +55 (11) 91234-5678 / +55 (45) 998244390
Website: enzobustos.github.io/POLI-PCS3643/

Agradecimentos:
Este projeto foi desenvolvido pelos alunos: Bruno Schio Falkemback, Adrian Oliveira, Antonio Fassini e Enzo Bustos da Escola Politécnica da USP como parte da disciplina PCS3643 - Laboratório de Engenharia de Software. Agradecemos a todos os colaboradores e professores que contribuíram para a realização deste projeto.

Observação: Esta documentação visa fornecer uma visão geral do funcionamento e das funcionalidades do site AedesWiki. Para detalhes técnicos específicos, recomenda-se consultar o código-fonte diretamente.
