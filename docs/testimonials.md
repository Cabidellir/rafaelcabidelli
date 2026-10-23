# Depoimentos: receção e publicação

A secção PT/EN não usa fotografias, contas ou publicação automática. O formulário reutiliza o endpoint Formspree já existente no contacto do portfólio: `https://formspree.io/f/mqpavado`. As mensagens são identificadas por `form_type=professional_testimonial` e um assunto próprio.

Antes de convidar colegas, confirmar no painel Formspree que este endpoint está ativo, os destinatários estão corretos e o plano permite o volume esperado. Não foi enviada uma mensagem de teste: a validação local não confirma a entrega de emails. A confirmação de envio é gerida pelo próprio Formspree. Limites e proteção contra spam dependem do serviço; o campo honeypot é apenas uma proteção adicional.

## Rever mensagens

1. Consultar a caixa de correio associada ao formulário ou o painel Formspree.
2. `publication_consent=private_only` significa feedback privado: nunca copiar essa mensagem nem os dados da pessoa para o repositório ou site.
3. `publication_consent=public_authorized` permite rever a publicação do texto e contexto fornecidos. Confirmar com a pessoa se houver dúvidas sobre identidade, relação profissional ou correções substanciais.
4. Não publicar email, dados de terceiros ou informação confidencial. Conservar a autorização num local privado, fora deste repositório público.
5. Não há painel de moderação no site. A publicação é manual, através dos dados estáticos abaixo. Não traduzir ou reescrever o depoimento sem concordância do autor.

## Publicar um depoimento autorizado

Adicionar a `assets/data/testimonials.json` apenas os dados públicos aprovados:

```json
{
  "id": "identificador-unico",
  "approved": true,
  "publicationConsent": true,
  "name": "Nome autorizado",
  "role": "Função opcional",
  "company": "Empresa ou projeto opcional",
  "relationship": "Relação profissional autorizada",
  "period": "Período em conjunto",
  "message": "Texto exato autorizado",
  "language": "pt"
}
```

O exemplo é apenas documentação; não representa um depoimento real. O ficheiro inicial está vazio. Executar `python scripts/build-testimonials.py`, rever PT/EN e publicar as páginas geradas. O script valida consentimento, aprovação, campos obrigatórios e IDs únicos, e escapa o texto como HTML. A autorização real deve ser conferida manualmente; os booleanos não a verificam automaticamente.

Os depoimentos mantêm o idioma original, identificado com `lang`, em ambas as páginas. Para remover um depoimento, eliminar o respetivo registo, regenerar as páginas e publicar. Nenhum dado de submissão é guardado no navegador ou no código do site.
