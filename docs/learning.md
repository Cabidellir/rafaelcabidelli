# Competências e formação / Skills and training

O site continua estático, com duas páginas HTML e o design Tailwind existente. A nova secção usa CSS local, SVG e JavaScript sem dependências. Não faz pedidos a APIs Microsoft em tempo de execução. A galeria e os dados do radar continuam disponíveis sem JavaScript; os filtros só aparecem quando o script funciona.

## Atualizar dados

1. Editar `assets/data/learning.json`: títulos PT/EN, data ISO, área principal, `partial` quando o título estiver cortado, e `verificationUrl` apenas quando existir uma ligação individual real. Não substituir uma ligação individual por um URL genérico de um curso.
2. Atualizar o retrato agregado apenas quando houver uma nova fonte datada. O retrato do PDF e o total de XP da galeria são conceitos separados.
3. Executar `python scripts/build-learning.py` e incluir as duas páginas HTML geradas no commit. Não editar diretamente o bloco `learning:start` / `learning:end`.

O gerador valida IDs únicos, datas, áreas, títulos e a correspondência da política XP com o texto apresentado. Não requer pacotes Python adicionais. Para mudar a política XP, atualizar a regra JSON, o gerador, os textos e a validação em conjunto.

## Proveniência e política

- Fonte: PDF `selos microsoft learn.pdf`, cinco páginas, captura de 21/10/2026. Não foi publicado porque contém um endereço de email pessoal.
- 32 selos de módulos transcritos; 9 troféus e nível 8 apenas no resumo. Nenhum troféu individual ou certificação foi inventado.
- Alguns títulos estão cortados na margem direita. São transcritos como excertos com reticências; traduções EN são editoriais e não nomes oficiais de credenciais.
- XP local: 1 por selo catalogado, atribuído a uma única área principal; zero por troféus, nível ou projetos. Não é o XP oficial Microsoft Learn e não mede proficiência.
- Radar: escala fixa de 0–32 selos por eixo, sem normalização ao maior valor. A concentração em Power BI reflete esta fonte, não uma avaliação comparativa de capacidade. Se uma área ultrapassar 32, rever a escala e o texto antes de publicar.
- Classificação editorial: Power BI 24; DAX 6; SQL 1; automação 1 (Power Apps); programação 0; cibersegurança 0. Segurança de modelos e de linhas pertence a BI, sem inferir qualificação em cibersegurança.
- O case existente é apresentado separadamente como evidência prática de BI, SQL e automação, sem XP. Está em português também quando referido pela página inglesa.
- Apenas Transact-SQL tem um URL individual fornecido na conversa anterior. A tentativa de validação automática desse URL não teve sucesso. As restantes ligações apontam para o perfil derivado do mesmo identificador público; não comprovam individualmente os módulos.

## Verificação e limites

Verificar PT/EN, filtros por área, estado vazio, reposição de todos os registos, seleção por teclado, nomes acessíveis, foco visível e larguras móvel/desktop. As datas são renderizadas a partir de ISO sem conversão de fuso horário.

O site existente depende de Tailwind CDN e Lucide remoto. Esta alteração não acrescenta bibliotecas de gráficos, fontes, imagens ou chamadas remotas. O JavaScript da nova secção é independente de Lucide.

Verificação realizada nesta alteração: contagem dos sete filtros (24/6/1/1/0/0/32), seleção SQL pelo radar, ativação DAX com Enter, estado inglês `1 training record`, ausência de transbordamento da secção a 375 e 1440 px, inspeção visual das duas disposições, sintaxe JavaScript, IDs/âncoras HTML e regeneração idempotente. Não foi executada uma auditoria completa com leitor de ecrã ou Lighthouse. A ligação de download do CV inglês foi corrigida para o PDF inglês que já existia no repositório.

## Melhorias futuras

Recolher ligações individuais de partilha e nomes completos dos títulos cortados; acrescentar projetos reproduzíveis para DAX/SQL e relatórios de testes para programação/cibersegurança; publicar transcrição redigida da fonte; compilar Tailwind localmente e fixar a versão de Lucide; adicionar auditoria automatizada de acessibilidade e desempenho.
