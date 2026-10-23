"""Render only manually approved, consented testimonials. No runtime dependency."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
records = json.loads((ROOT / 'assets/data/testimonials.json').read_text(encoding='utf-8'))
for record in records:
    assert record.get('approved') is True and record.get('publicationConsent') is True, 'Only approved, consented records belong in this public file'
    assert all(record.get(key) for key in ['id', 'name', 'relationship', 'period', 'message', 'language'])
    assert record['language'] in ['pt', 'en']
assert len({r['id'] for r in records}) == len(records)

for language, filename in [('pt', 'index.html'), ('en', 'index_en.html')]:
    def t(pt, en): return en if language == 'en' else pt
    cards = ''
    for record in records:
        company = f' · {escape(record["company"])}' if record.get('company') else ''
        role = f' · {escape(record["role"])}' if record.get('role') else ''
        cards += f'<figure class="testimonial"><blockquote lang="{record["language"]}">{escape(record["message"])}</blockquote><figcaption><strong>{escape(record["name"])}</strong>{role}<br>{escape(record["relationship"])}{company}<br>{escape(record["period"])}</figcaption></figure>\n'
    if not cards:
        cards = f'<div class="testimonials-panel"><h3>{t("Já trabalhámos juntos?", "Have we worked together?")}</h3><p>{t("Conta como foi partilharmos a operação, um projeto ou uma equipa. Um exemplo concreto pode ajudar outras pessoas a conhecer a minha forma de trabalhar.", "Share your experience of working with me in an operation, a project or a team. A concrete example can help others understand how I work.")}</p><small>{t("Os depoimentos serão apresentados aqui após autorização e revisão. Não são publicados automaticamente.", "Testimonials will appear here after permission and review. Nothing is published automatically.")}</small></div>'
    section = f'''<!-- testimonials:start -->
    <section id="testimonials" class="testimonials" aria-labelledby="testimonials-title">
      <h2 id="testimonials-title">{t('Quem trabalhou comigo', 'People I have worked with')}</h2>
      <p>{t('Experiências partilhadas por quem fez parte do meu percurso profissional.', 'Experiences shared by people from my professional journey.')}</p>
      <div class="testimonials-layout"><div>{cards}</div>
        <div class="testimonials-panel"><h3>{t('Partilhar um depoimento', 'Share a testimonial')}</h3>
          <p id="testimonial-help">{t('Podes autorizar a publicação ou enviar feedback apenas para mim. Campos com * são obrigatórios.', 'You can allow publication or send feedback just to me. Fields marked * are required.')}</p>
          <form action="https://formspree.io/f/mqpavado" method="POST" aria-describedby="testimonial-help testimonial-privacy">
            <input type="hidden" name="form_type" value="professional_testimonial">
            <input type="hidden" name="_subject" value="Portfolio: novo depoimento / new testimonial">
            <input type="hidden" name="language" value="{language}">
            <div class="trap" aria-hidden="true"><label for="testimonial-trap">Leave empty</label><input id="testimonial-trap" type="text" name="_gotcha" tabindex="-1" autocomplete="off"></div>
            <label for="testimonial-name">{t('Nome a apresentar *', 'Display name *')}</label><input id="testimonial-name" name="name" required maxlength="100" autocomplete="name">
            <label for="testimonial-email">{t('Email para contacto *', 'Contact email *')}</label><input id="testimonial-email" name="email" type="email" required maxlength="254" autocomplete="email" aria-describedby="email-note"><small id="email-note">{t('Usado para esclarecer ou confirmar o depoimento. Não será publicado.', 'Used to clarify or confirm your testimonial. It will not be published.')}</small>
            <label for="testimonial-role">{t('Função (opcional)', 'Role (optional)')}</label><input id="testimonial-role" name="role" maxlength="120" autocomplete="organization-title">
            <label for="testimonial-company">{t('Empresa ou projeto (opcional)', 'Company or project (optional)')}</label><input id="testimonial-company" name="company" maxlength="120" autocomplete="organization">
            <label for="testimonial-relationship">{t('Como trabalhámos juntos? *', 'How did we work together? *')}</label><select id="testimonial-relationship" name="relationship" required><option value="">{t('Selecionar', 'Select')}</option><option value="colleague">{t('Colega de equipa', 'Team colleague')}</option><option value="manager">{t('Fui responsável pela tua equipa', 'I managed your team')}</option><option value="team_member">{t('Fiz parte de uma equipa que lideraste', 'I was on a team you led')}</option><option value="project_partner">{t('Parceiro de projeto', 'Project partner')}</option><option value="other">{t('Outra relação profissional', 'Other professional relationship')}</option></select>
            <label for="testimonial-period">{t('Período em que trabalhámos juntos *', 'When did we work together? *')}</label><input id="testimonial-period" name="period" required maxlength="100" placeholder="{t('Ex.: 2019–2021', 'E.g. 2019–2021')}">
            <label for="testimonial-message">{t('O teu depoimento *', 'Your testimonial *')}</label><textarea id="testimonial-message" name="message" rows="5" required minlength="20" maxlength="2000" aria-describedby="message-note"></textarea><small id="message-note">{t('Entre 20 e 2000 caracteres. Evita dados de terceiros ou informações confidenciais das empresas.', 'Between 20 and 2000 characters. Avoid third-party personal data or confidential company information.')}</small>
            <fieldset><legend>{t('Como posso usar a mensagem? *', 'How may I use your message? *')}</legend>
              <label class="choice"><input type="radio" name="publication_consent" value="private_only" checked required><span>{t('Apenas para o Rafael. Não autorizo a publicação.', 'Only for Rafael. I do not allow publication.')}</span></label>
              <label class="choice"><input type="radio" name="publication_consent" value="public_authorized" required><span>{t('Autorizo a publicação no portfólio do meu depoimento, nome e contexto profissional preenchido, após revisão do Rafael. O email permanece privado.', 'I allow my testimonial, name and supplied professional context to be published in the portfolio after Rafael reviews it. My email stays private.')}</span></label>
            </fieldset>
            <p id="testimonial-privacy"><small>{t('O formulário envia os dados ao Rafael através do Formspree. Podes pedir esclarecimentos ou a remoção de um depoimento através de rafaelcabidelli@gmail.com. Ao enviar, sairás para a confirmação do Formspree.', 'This form sends your details to Rafael through Formspree. For questions or testimonial removal, contact rafaelcabidelli@gmail.com. Submitting opens the Formspree confirmation page.')}</small></p>
            <button type="submit">{t('Enviar para revisão', 'Send for review')}</button>
          </form>
        </div>
      </div>
    </section>
    <!-- testimonials:end -->'''
    path = ROOT / filename
    html = path.read_text(encoding='utf-8')
    if '<!-- testimonials:start -->' in html:
        start = html.index('<!-- testimonials:start -->')
        end = html.index('<!-- testimonials:end -->') + len('<!-- testimonials:end -->')
        html = html[:start] + section + html[end:]
    else:
        html = html.replace('    <footer id="contact"', section + '\n\n    <footer id="contact"')
        html = html.replace('</head>', '    <link rel="stylesheet" href="assets/css/testimonials.css">\n</head>')
        link = f'<a href="#testimonials" class="text-slate-600 hover:text-blue-900 font-medium">{t("Depoimentos", "Testimonials")}</a>'
        html = html.replace('<a href="#experience" class="text-slate-600', link + '\n                    <a href="#experience" class="text-slate-600', 1)
        mobile = f'<a href="#testimonials" onclick="toggleMenu()" class="block text-lg font-medium text-slate-700">{t("Depoimentos", "Testimonials")}</a>'
        html = html.replace('<a href="#experience" onclick=', mobile + '\n                <a href="#experience" onclick=', 1)
        html = html.replace('space-x-8 items-center', 'space-x-5 items-center')
        nav_start = html.index('<nav ')
        nav_end = html.index('</nav>', nav_start)
        html = html[:nav_start] + html[nav_start:nav_end].replace('md:', 'lg:') + html[nav_end:]
    path.write_text(html, encoding='utf-8')
