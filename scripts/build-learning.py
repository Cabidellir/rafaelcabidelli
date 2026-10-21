"""Generate both static, crawlable learning sections from editable JSON. Python stdlib only."""
import json
import math
from datetime import date
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'assets/data/learning.json').read_text(encoding='utf-8'))
skills = json.loads((ROOT / 'assets/data/skills.json').read_text(encoding='utf-8'))
areas = ['bi', 'dax', 'sql', 'automation', 'programming', 'security']
assert [a['id'] for a in skills['areas']] == areas
assert [stage['value'] for stage in skills['stages']] == [0, 1, 2, 3, 4]
for skill in skills['areas']:
    assert type(skill['stage']) is int and 0 <= skill['stage'] <= 4
    assert skill['pt'] and skill['en'] and skill['sourcePt'] and skill['sourceEn']
assert len({r['id'] for r in data['badges']}) == len(data['badges']), 'Duplicate badge IDs'
assert data['xpRule'] == {'pointsPerBadge': 1, 'pointsPerTrophy': 0, 'pointsPerProject': 0}, 'Update the displayed rule and generator together when changing XP policy'
for record in data['badges']:
    assert record['area'] in areas
    date.fromisoformat(record['date'])
    assert record['pt'] and record['en']
for lang, file in [('pt', 'index.html'), ('en', 'index_en.html')]:
    en = lang == 'en'
    def t(pt, eng): return eng if en else pt
    labels = ['Power BI', 'DAX', 'SQL', t('Automação', 'Automation'), t('Programação', 'Programming'), t('Cibersegurança', 'Cybersecurity')]
    levels = [skill['stage'] for skill in skills['areas']]
    stage_names = [stage[lang] for stage in skills['stages']]
    skill_summary = '; '.join(f'{label}: {stage_names[level]}' for label,level in zip(labels,levels))
    def point(i, radius):
        angle = math.pi * i / 3 - math.pi / 2
        return f'{220 + radius * math.cos(angle):.2f},{190 + radius * math.sin(angle):.2f}'
    grid = ''.join(f'<polygon points="{" ".join(point(i, radius) for i in range(6))}" fill="none" stroke="#cbd5e1"/>' for radius in [33.75, 67.5, 101.25, 135])
    grid += ''.join(f'<text x="226" y="{190-radius+12}" aria-hidden="true">{i}</text>' for i,radius in enumerate([33.75,67.5,101.25,135],1))
    axes = ''.join(f'<line x1="220" y1="190" x2="{point(i,135).split(",")[0]}" y2="{point(i,135).split(",")[1]}" stroke="#cbd5e1"/><text x="{point(i,165).split(",")[0]}" y="{point(i,165).split(",")[1]}" text-anchor="middle">{label}</text>' for i,label in enumerate(labels))
    polygon = ' '.join(point(i, 135 * levels[i] / 4) for i in range(6))
    summary = ''.join(f'<div><strong>{value}</strong>{label}</div>' for value,label in [(data['snapshot']['badges'], t('selos Microsoft Learn','Microsoft Learn badges')), (data['snapshot']['trophies'],t('troféus Microsoft Learn','Microsoft Learn trophies')), (data['snapshot']['level'],t('nível Microsoft Learn','Microsoft Learn level')), (len(data['badges']),t('XP de formação','training XP'))])
    buttons = ''.join(f'<button type="button" data-area="{a}" aria-pressed="false" aria-controls="learn-evidence">{label}</button>' for a,label in zip(areas,labels))
    filters = ''.join(f'<button type="button" data-filter="{a}" aria-pressed="{str(a=="all").lower()}" aria-controls="learn-gallery">{label}</button>' for a,label in [('all',t('Todas','All'))]+list(zip(areas,labels)))
    cards = ''
    for r in data['badges']:
        title = r['en'] if en else r['pt']
        date = r['date']
        note = t('Título cortado no PDF; excerto transcrito.', 'Title clipped in PDF; transcribed excerpt.') if r.get('partial') else ''
        url = r.get('verificationUrl')
        link = f'<a href="{e(url)}">{t("Abrir conquista Microsoft Learn","Open Microsoft Learn achievement")}</a>' if url else f'<a href="{e(data["profileUrl"])}">{t("Consultar perfil Microsoft Learn","View Microsoft Learn profile")}</a><small>{t("Sem ligação individual; conclusão documentada no PDF.","No individual link; completion documented in PDF.")}</small>'
        cards += f'<li class="learn-card" data-area="{r["area"]}"><small>Microsoft Learn · {t("Selo de módulo","Module badge")}</small><h4>{e(title)}</h4><small>{t("Concluído em","Completed on")} <time datetime="{date}">{date[8:10]}/{date[5:7]}/{date[:4]}</time> · 1 XP</small>{f"<p class=learn-note>{note}</p>" if note else ""}{link}</li>'
    panels = ''
    for skill,label in zip(skills['areas'],labels):
        links = ' · '.join(f'<a href="{e(link["url"])}">{e(link["label"])}</a>' for link in skill['links'])
        panels += f'<article class="skill-evidence" data-evidence="{skill["id"]}"><h4>{label} · {e(stage_names[skill["stage"]])}</h4><p>{e(skill[lang])}</p><p class="learn-note">{e(skill["sourceEn" if en else "sourcePt"])}</p>{links}</article>'
    legend = ''.join(f'<li><strong>{stage["value"]} · {e(stage[lang])}</strong> — {description}</li>' for stage,description in zip(skills['stages'][1:], [t('estudo e contacto inicial com o tema', 'study and initial exposure'), t('aplicação em projetos, exercícios ou iniciativas concretas', 'application in projects, exercises or concrete initiatives'), t('uso repetido em vários projetos ou no trabalho diário', 'repeated use across projects or in daily work'), t('resolução de problemas complexos em contextos variados, com decisões técnicas justificadas e resultados demonstráveis', 'solving complex problems across varied contexts, with justified technical decisions and demonstrable results')]))
    section = f'''<!-- learning:start -->
    <section id="learning" class="learning" aria-labelledby="learn-title">
      <h2 id="learn-title">{t('Habilidades e experiência','Skills and experience')}</h2>
      <p>{t('Um retrato da minha experiência em dados, automação e tecnologia, reunindo prática profissional, projetos e formação.','A view of my experience in data, automation and technology, bringing together professional practice, projects and training.')}</p>
      <div class="learn-layout">
        <div class="learn-panel"><h3>{t('Radar de Habilidades','Skills Radar')}</h3>
          <svg class="learn-radar" viewBox="0 0 440 380" role="img" aria-labelledby="radar-title radar-desc"><title id="radar-title">{t('Contexto de prática por habilidade','Practice context by skill')}</title><desc id="radar-desc">{e(skill_summary)}. {t('Autoavaliação contextual em quatro patamares; sem percentagens de domínio técnico.','Contextual self-assessment in four stages; no technical mastery percentages.') }</desc>{grid}{axes}<polygon points="{polygon}" fill="#2563eb" fill-opacity=".18" stroke="#1e3a8a" stroke-width="2"/></svg>
          <p class="learn-note">{t('1 · Fundamentos / 2 · Aplicação prática / 3 · Prática recorrente / 4 · Prática avançada', '1 · Foundations / 2 · Practical application / 3 · Recurring practice / 4 · Advanced practice')}</p>
          <p class="learn-note">{t('Selecione uma habilidade para conhecer a experiência que sustenta o gráfico. A galeria de formação tem filtros independentes.','Select a skill to explore the experience behind the chart. The training gallery has independent filters.')}</p>
          <div class="learn-area-list learn-controls" hidden aria-label="{t('Áreas do radar','Radar areas')}">{buttons}</div>
          <p>{e(skill_summary)}</p>
        </div>
        <div class="learn-panel"><h3>{t('Experiência por trás do radar','Experience behind the radar')}</h3>
          <p class="learn-note">{t('Autoavaliação contextual, atualizada em 22/10/2026. Os patamares descrevem o contexto de prática; não são notas, certificações ou uma avaliação independente de proficiência.','Contextual self-assessment, updated on 22 October 2026. Stages describe practice context; they are not scores, certifications or an independent proficiency assessment.')}</p>
          <div id="learn-evidence" aria-live="polite">{panels}</div>
          <details><summary>{t('Como ler os patamares','How to read the stages')}</summary><ol class="skill-legend">{legend}</ol><p>{t('Mesmo o patamar 4 não significa conhecimento completo: há sempre espaço para evoluir. O centro representa ausência de contexto registado. A posição depende da experiência descrita, sem somar horas, selos, linguagens ou repositórios. O mesmo patamar pode incluir diferentes tempos de experiência e níveis de complexidade. SQL é uma prática diária recente; a participação no Hacker Rangers refere-se a sensibilização e boas práticas.','Even stage 4 does not mean complete knowledge: there is always room to grow. The centre represents no recorded context. Position depends on the experience described, without adding hours, badges, languages or repositories. The same stage can include different experience durations and complexity levels. SQL is recent daily practice; Hacker Rangers participation concerns awareness and good practices.')}</p></details>
        </div>
      </div>
      <h3>{t('Galeria de formação','Training gallery')}</h3>
      <div class="learn-summary">{summary}</div>
      <p class="learn-note">{t('Retrato de 21/10/2026, segundo o PDF Microsoft Learn. Selos e troféus de aprendizagem não são certificações profissionais.','Snapshot dated 21 October 2026, from the Microsoft Learn PDF. Learning badges and trophies are not professional certifications.')}</p>
      <p class="learn-note">{t('XP de formação do portfólio: 1 por selo catalogado, sem bónus por troféus, nível ou projetos. É diferente do XP oficial Microsoft Learn e não altera o Radar de Habilidades.','Portfolio training XP: 1 per catalogued badge, with no bonus for trophies, level or projects. It is separate from official Microsoft Learn XP and does not affect the Skills Radar.')}</p>
          <details><summary>{t('Fontes e limites de verificação','Sources and verification limits')}</summary><p>{t('Os 32 selos foram transcritos do PDF fornecido. Os 9 troféus aparecem apenas no total: os nomes não constam destas páginas. Alguns títulos estão cortados e mantêm reticências. As traduções inglesas são editoriais.','The 32 badges were transcribed from the supplied PDF. The 9 trophies appear only as a total: their names are absent from these pages. Some titles are clipped and retain ellipses. English translations are editorial.')}</p><p>{t('A ligação individual de Transact-SQL foi fornecida pelo autor; não foi possível validá-la automaticamente. As restantes ligações abrem o perfil para consulta, sem afirmar verificação individual.','The author supplied the individual Transact-SQL link; automated validation was unavailable. Other links open the profile for review and do not claim individual verification.')}</p><a href="{e(data['profileUrl'])}">{t('Consultar conquistas no Microsoft Learn','Review Microsoft Learn achievements')}</a></details>
      <div class="learn-filters learn-controls" hidden aria-label="{t('Filtrar formação por área','Filter training by area')}">{filters}</div>
      <p id="learn-results" role="status">{len(data["badges"])} {t('registos de formação','training records')}</p>
      <p id="learn-empty" hidden>{t('Ainda sem formação catalogada nesta área. Consulte os projetos para outras evidências.','No training catalogued in this area yet. See projects for other evidence.')}</p>
      <ul id="learn-gallery" class="learn-gallery">{cards}</ul>
    </section>
    <!-- learning:end -->'''
    path = ROOT / file
    html = path.read_text(encoding='utf-8')
    if '<!-- learning:start -->' in html:
        start = html.index('<!-- learning:start -->')
        end = html.index('<!-- learning:end -->') + len('<!-- learning:end -->')
        html = html[:start] + section + html[end:]
    else:
        html = html.replace('    <section id="experience"', section + '\n\n    <section id="experience"')
        html = html.replace('</head>', '    <link rel="stylesheet" href="assets/css/learning.css">\n    <script defer src="assets/js/learning.js"></script>\n</head>')
        html = html.replace('href="#skills"', 'href="#learning"')
        html = html.replace('Power BI Expert', 'Power BI')
        html = html.replace('lucide.createIcons();', 'if (window.lucide) lucide.createIcons();')
    path.write_text(html, encoding='utf-8')
