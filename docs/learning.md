# Radar de Habilidades e formação

O radar representa uma autoavaliação contextual da prática, reunindo experiência profissional declarada, projetos públicos e formação. Não representa contagem de selos, percentagens de domínio ou certificação de proficiência.

## Dados editáveis

- `assets/data/skills.json`: patamares, descrições PT/EN, fontes e ligações por habilidade.
- `assets/data/learning.json`: formação Microsoft Learn, datas ISO, títulos e URLs individuais quando disponíveis.
- Executar `python scripts/build-learning.py` e incluir as duas páginas geradas no commit. O gerador usa apenas a biblioteca padrão Python e valida IDs, datas, áreas, patamares e política XP.
- Não editar diretamente os blocos `learning:start` / `learning:end`. Ao rever a avaliação, atualizar a data no JSON e no texto do gerador.

## Critério do radar

Escala ordinal de contexto de prática: 1 = fundamentos (estudo/contacto inicial); 2 = aplicação prática (projetos, exercícios ou iniciativas concretas); 3 = prática recorrente (vários projetos ou uso diário no trabalho). 4 = prática avançada (problemas complexos em contextos variados, decisões técnicas justificadas e resultados demonstráveis). O patamar 4 não significa conhecimento completo. Os níveis atuais permanecem em 3 ou 2, com espaço visual para evolução. O centro, 0, é ausência de contexto registado, não incapacidade.

Avaliação de 22/10/2026:

| Área | Patamar | Justificação |
|---|---|---|
| Power BI | 3 | Vários dashboards operacionais declarados; case de ocupação publicado |
| DAX | 3 | Aplicação em vários relatórios de picking accuracy e ocupação declarada; sem amostra pública específica de fórmulas |
| SQL | 3 | Uso diário durante cerca de seis meses na ID Logistics declarado; área recente; case com SQL e formação |
| Automação | 3 | Excel/Access e Power Automate online/desktop declarados; case de integração publicado |
| Programação | 2 | Scripts públicos no Sabedoria Simples e 241 Solutions; C2L em desenvolvimento |
| Cibersegurança | 2 | Jogos e melhorias Hacker Rangers na Americanas; segundo lugar interno nacional declarado, sem comprovativo público associado |

O mesmo patamar não significa o mesmo tempo de experiência, complexidade ou domínio técnico. Hacker Rangers descreve sensibilização e boas práticas, sem certificar pentesting. Código disponível não comprova autoria integral, autonomia ou domínio de todas as tecnologias. Não foram executados ou auditados os projetos externos.

Foram inspecionados os scripts JavaScript públicos de Cabidellir/sabedoriasimples e Cabidellir/twoforonesolutions, README e estrutura de crates de Cabidellir/C2L-Antivirus. O README C2L indica fase inicial de definição/arquitetura: não se afirma proteção validada ou funcionalidades futuras como entregues. Forks e número de repositórios não determinam patamares.

## Formação e XP

O XP local é exclusivo da galeria: 1 por selo catalogado, sem bónus por troféus, nível ou projetos. Não altera o radar e difere do XP oficial Microsoft Learn.

Fonte: PDF selos microsoft learn.pdf, cinco páginas, captura de 21/10/2026. Foram transcritos 32 selos; 9 troféus e nível 8 constam apenas do resumo. Títulos cortados conservam reticências e traduções EN são editoriais. Apenas Transact-SQL tem ligação individual fornecida, cuja validação automática não foi possível. Restantes URLs abrem o perfil, sem afirmar verificação individual. O PDF não foi publicado por conter email pessoal.

## Interface e verificação

A seleção de habilidades mostra experiência e fontes; os filtros afetam exclusivamente a formação. Sem JavaScript, todas as experiências e a galeria continuam em HTML estático. SVG e resumo textual descrevem o gráfico; botões têm foco visível e estados de seleção. Não há dependências novas ou APIs em tempo de execução. As dependências CDN preexistentes permanecem.

Verificar PT/EN, independência radar/galeria, seleção das seis habilidades, filtros, estados vazios, teclado, larguras móvel/desktop e regeneração idempotente. Não equivale a auditoria completa com leitor de ecrã ou Lighthouse.

Melhorias futuras: exemplos DAX anonimizados, case de macros/Power Automate Desktop e comprovativo Hacker Rangers; complementar com tarefas demonstráveis. Rever os patamares com novos exemplos, sem aumentar notas automaticamente.
