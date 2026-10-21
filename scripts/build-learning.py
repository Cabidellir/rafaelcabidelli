"""Generate both static, crawlable learning sections from editable JSON. Python stdlib only."""
import json
import math
from datetime import date
from html import escape as e
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'assets/data/learning.json').read_text(encoding='utf-8'))
areas = ['bi', 'dax', 'sql', 'automation', 'programming', 'security']
assert len({r['id'] for r in data['badges']}) == len(data['badges']), 'Duplicate badge IDs'
assert data['xpRule'] == {'pointsPerBadge': 1, 'pointsPerTrophy': 0, 'pointsPerProject': 0, 'radarMax': 32}, 'Update the displayed rule and generator together when changing XP policy'
for record in data['badges']:
    assert record['area'] in areas
    date.fromisoformat(record['date'])
    assert record['pt'] and record['en']
for lang, file in [('pt', 'index.html'), ('en', 'index_en.html')]:
    en = lang == 'en'
    def t(pt, eng): return eng if en else pt
    labels = ['Power BI', 'DAX', 'SQL', t('Automação', 'Automation'), t('Programação', 'Programming'), t('Cibersegurança', 'Cybersecurity')]
    counts = [sum(r['area'] == a for r in data['badges']) for a in areas]
    assert max(counts) <= data['xpRule']['radarMax'], 'Review radar scale and labels before publishing additional badges'
    def point(i, radius):
        angle = math.pi * i / 3 - math.pi / 2
        return f'{220 + radius * math.cos(angle):.2f},{190 + radius * math.sin(angle):.2f}'
    grid = ''.join(f'<polygon points="{" ".join(point(i, radius) for i in range(6))}" fill="none" stroke="#cbd5e1"/>' for radius in [45, 90, 135])
    axes = ''.join(f'<line x1="220" y1="190" x2="{point(i,135).split(",")[0]}" y2="{point(i,135).split(",")[1]}" stroke="#cbd5e1"/><text x="{point(i,165).split(",")[0]}" y="{point(i,165).split(",")[1]}" text-anchor="middle">{label}</text>' for i,label in enumerate(labels))
    polygon = ' '.join(point(i, 135 * counts[i] / 32) for i in range(6))
    summary = ''.join(f'<div><strong>{value}</strong>{label}</div>' for value,label in [(data['snapshot']['badges'], t('selos Microsoft Learn','Microsoft Learn badges')), (data['snapshot']['trophies'],t('troféus Microsoft Learn','Microsoft Learn trophies')), (data['snapshot']['level'],t('nível Microsoft Learn','Microsoft Learn level')), (len(data['badges']),t('XP do portfólio','portfolio XP'))])
    buttons = ''.join(f'<button type="button" data-area="{a}" aria-pressed="false" aria-controls="learn-gallery learn-evidence">{label} · {count} XP</button>' for a,label,count in zip(areas,labels,counts))
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
    for a,label,count in zip(areas,labels,counts):
        project = f'<a href="projects/ocupacao-bi/index.html">{t("Ver case de automação e BI (português)","View automation and BI case (Portuguese)")}</a>' if a in ['bi','sql','automation'] else ''
        badge_label = t('selo catalogado' if count == 1 else 'selos catalogados', 'catalogued badge' if count == 1 else 'catalogued badges')
        panels += f'<div data-evidence="{a}" hidden><h3>{label}</h3><p>{count} {badge_label}; {t("não é uma avaliação de proficiência.","this is not a proficiency assessment.")}</p>{project}<p>{t("A formação e os projetos são evidências distintas. Sem avaliação independente de proficiência publicada.","Training and projects are separate evidence. No independent proficiency assessment published.")}</p></div>'
    section = f'''<!-- learning:start -->
    <section id="learning" class="learning" aria-labelledby="learn-title">
      <h2 id="learn-title">{t('Competências em evolução','Skills in progress')}</h2>
      <p>{t('Um mapa do meu percurso de aprendizagem, inspirado num RPG. Cada conquista tem uma origem; a prática está nos projetos.','An RPG-inspired map of my learning journey. Every achievement has a source; practical work lives in the projects.')}</p>
      <div class="learn-summary">{summary}</div>
      <p class="learn-note">{t('Retrato de 21/10/2026, segundo o PDF Microsoft Learn. Selos e troféus de aprendizagem não são certificações profissionais.','Snapshot dated 21 October 2026, from the Microsoft Learn PDF. Learning badges and trophies are not professional certifications.')}</p>
      <div class="learn-layout">
        <div class="learn-panel"><h3>{t('Radar de aprendizagem','Learning radar')}</h3>
          <svg class="learn-radar" viewBox="0 0 440 380" role="img" aria-labelledby="radar-title radar-desc"><title id="radar-title">{t('Distribuição dos selos por área','Badge distribution by area')}</title><desc id="radar-desc">{'; '.join(f'{label}: {count}' for label,count in zip(labels,counts))}. {t('Escala fixa de 0 a 32 selos por eixo; não mede proficiência.','Fixed scale of 0 to 32 badges per axis; does not measure proficiency.')}</desc>{grid}{axes}<polygon points="{polygon}" fill="#2563eb" fill-opacity=".18" stroke="#1e3a8a" stroke-width="2"/></svg>
          <p class="learn-note">{t('Escala: 0–32 selos por eixo. Selecione uma área para explorar as evidências e filtrar a galeria.','Scale: 0–32 badges per axis. Select an area to explore evidence and filter the gallery.')}</p>
          <div class="learn-area-list learn-controls" hidden aria-label="{t('Áreas do radar','Radar areas')}">{buttons}</div>
          <p>{' · '.join(f'{label}: {count}' for label,count in zip(labels,counts))}</p>
        </div>
        <div class="learn-panel"><h3>{t('Progresso com contexto','Progress with context')}</h3>
          <p>{t('XP do portfólio: 1 ponto por selo de módulo catalogado, atribuído a uma única área principal. Sem bónus por troféus, projetos ou nível. O total é calculado a partir da galeria.','Portfolio XP: 1 point per catalogued module badge, assigned to one primary area. No bonus for trophies, projects or level. The total is calculated from the gallery.')}</p>
          <p>{t('Este XP é uma regra gamificada local, diferente do XP oficial Microsoft Learn. Não equivale a experiência profissional, certificação ou domínio técnico. Zero significa ausência de selos catalogados nesta área, não ausência de capacidade.','This XP is a local game rule, separate from official Microsoft Learn XP. It does not represent professional experience, certification or technical mastery. Zero means no catalogued badges in this area, not a lack of ability.')}</p>
          <div id="learn-evidence" aria-live="polite">{panels}</div>
          <details><summary>{t('Fontes e limites de verificação','Sources and verification limits')}</summary><p>{t('Os 32 selos foram transcritos do PDF fornecido. Os 9 troféus aparecem apenas no total: os nomes não constam destas páginas. Alguns títulos estão cortados e mantêm reticências. As traduções inglesas são editoriais.','The 32 badges were transcribed from the supplied PDF. The 9 trophies appear only as a total: their names are absent from these pages. Some titles are clipped and retain ellipses. English translations are editorial.')}</p><p>{t('A ligação individual de Transact-SQL foi fornecida pelo autor; não foi possível validá-la automaticamente. As restantes ligações abrem o perfil para consulta, sem afirmar verificação individual.','The author supplied the individual Transact-SQL link; automated validation was unavailable. Other links open the profile for review and do not claim individual verification.')}</p><a href="{e(data['profileUrl'])}">{t('Consultar conquistas no Microsoft Learn','Review Microsoft Learn achievements')}</a></details>
        </div>
      </div>
      <h3>{t('Galeria de formação','Training gallery')}</h3>
      <div class="learn-filters learn-controls" hidden aria-label="{t('Filtrar formação por área','Filter training by area')}">{filters}</div>
      <p id="learn-results" role="status">32 {t('registos de formação','training records')}</p>
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
