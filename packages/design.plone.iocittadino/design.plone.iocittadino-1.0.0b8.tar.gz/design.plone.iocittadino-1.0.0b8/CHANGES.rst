Changelog
=========

1.0.0b8 (2024-03-05)
--------------------
- Aggiunto modo per aggiungere campi al messaggio e al suo serializer registrando 
  delle utility per interfacce predefinite
  [lucabel]

1.0.0b7 (unreleased)
--------------------

- Fix the PDF Report + new survey field type added to pdf generation: radiogroup
  [folix-01]
- Fix: #49945 l'areaopeartore va in errore se il modello pratica è stato cancellato
  (Aggiunto workaround per non mandare in errore, serve però che i dati siano in qualche modo
  recuperabili anche se il modello è stato eliminato)
  [mamico]
- Aggiunto modo per aggiungere campi alla pratica e al suo serializer registrando 
  delle utility per interfacce predefinite
  [lucabel]

1.0.0b6 (2023-10-25)
--------------------

- Allow users to retrieve their own messages also if ModelloPratica is private.
  [cekk]


1.0.0b5 (2023-08-31)
--------------------
- Manage blobs as a storage field
  [folix-01]
- Use named form fields as user's onceonly data
  [folix-01]
- next_steps non definito == non iterable
  [mamico]

- allegati messaggi sono blob nello storage soup
  [mamico]

- allegati nei messaggi
  [folix-01]

- monkey patch per c.mailfromfield per mandare
  inviare messaggi quando si inviano mail associati a prenotazioni
  [mamico]


1.0.0b4 (2023-06-16)
--------------------

- Add title to message serializer.
  [folix-01]


1.0.0b3 (2023-06-16)
--------------------

- Add pratica_model from model on create
  [mamico]


1.0.0b2 (2023-06-16)
--------------------

- Add possibility to relate message to the object.
  [folix-01]

1.0.0b1 (2023-05-18)
--------------------

- Nothing changed yet.


1.0.0a29 (2023-05-03)
---------------------

- Add list of unique services in @pratiche endpoint.
  [cekk]
- Handle missing pratica in message serializer.
  [cekk]

1.0.0a28 (2023-04-28)
---------------------

- Add profile (*demo_contents*) that loads a set of example contents.
  [cekk]
- Create message on pratica creation instead of mail sending.
  [roman.kysil]
- Disallow multiple pratica creation for the same Model.
  [cekk]
- Optionally send model schema in Pratica serializer.
  [cekk]
- Improve pratica_id checks on Message and soup getter.
  [cekk]
- Create user store to store onceonly fields.
  [cekk]

1.0.0a27 (2023-03-21)
---------------------

- Add domain to translation messages.
  [roman.kysil]


1.0.0a26 (2023-03-21)
---------------------

- Raise Unauthorized if anonymous can serializer ModelloPratica even if it's published.
  [cekk]
- Remove group serializer customization, and add a new endpoint (@operatori_pratica) to get list of group members.
  [cekk]


1.0.0a25 (2023-03-20)
---------------------

- Remove pdb.
  [roman.kysil]


1.0.0a24 (2023-03-20)
---------------------

- Fix translations.
  [roman.kysil]


1.0.0a23 (2023-03-20)
---------------------

- Update locales.
  [roman.kysil]


1.0.0a22 (2023-03-20)
---------------------

- Update locales.
  [roman.kysil]


1.0.0a21 (2023-03-20)
---------------------

- Fixed transtations.
  [roman.kysil]


1.0.0a20 (2023-03-20)
---------------------

- Update locales
  [roman.kysil]

1.0.0a110 (2023-03-20)
----------------------

- Fix pratica transition notify.
  [roman.kysil]


1.0.0a19 (2023-03-17)
---------------------

- Fix csrf for endpoints.
  [cekk]

1.0.0a18 (2023-03-17)
---------------------

- Add pratica.has_report field to serializer
  [roman.kysil]
- Add translations.
  [cekk]
- Fix update Pratica logic.
  [cekk]


1.0.0a17 (2023-03-17)
---------------------

- Do not delete pratica if it's not in draft state.
  [cekk]


1.0.0a16 (2023-03-17)
---------------------

- Handle nonexitent pdf record on pratica.
  [roman.kysil]


1.0.0a15 (2023-03-16)
---------------------

- Add pdf extension to pratica report files.
  [roman.kysil]


1.0.0a14 (2023-03-16)
---------------------

- Remove unused serializer for next_steps.
  [cekk]
- Add available_states to pratica serializer.
  [cekk]
- Change pratica report generation technique (moved to frontend)
  [roman.kysil]

1.0.0a13 (2023-03-15)
---------------------

- Fix wrong release.
  [cekk]

1.0.0a12 (2023-03-14)
---------------------

- Fix sort users in groups endpoint.
  [cekk]

1.0.0a11 (2023-03-10)
---------------------

- Create Operatori pratiche group on install.
  [cekk]
- Customize @groups endpoint to show also fullnames.
  [cekk]
- Add new field for pratica: assigned_to.
  [cekk]


1.0.0a10 (2023-03-01)
---------------------

- Fix pratica_report view and expose the download url in restapi endpoints.
  [cekk]

1.0.0a9 (2023-03-01)
--------------------

- Fix email send process and template.
  [cekk]

1.0.0a8 (2023-03-01)
--------------------

- Change field from Int to TextString.
  [cekk]


1.0.0a5 (2023-02-27)
--------------------

- Nothing changed yet.


1.0.0a4 (2023-02-20)
--------------------

- Nothing changed yet.


1.0.0a3 (2023-01-24)
--------------------

- Nothing changed yet.


1.0.0a2 (2023-01-24)
--------------------

- Nothing changed yet.


1.0.0a1 (2023-01-24)
--------------------

- Initial release.
  []
