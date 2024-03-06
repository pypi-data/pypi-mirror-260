.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://gitlab.com/redturtle/io-comune/design.plone.iocittadino/badges/master/coverage.svg

.. image:: https://gitlab.com/redturtle/io-comune/design.plone.iocittadino/badges/master/pipeline.svg

.. image:: https://gitlab.com/redturtle/io-comune/design.plone.iocittadino/-/badges/release.svg


============
Io-Cittadino
============

Io-Cittadino è un add-on per l'ecosistema Io-Comune per gestire i servizi online di un ente.

Funzionamento
=============

E' presente un nuovo content-type "Modello Pratica" che serve a definire appunto il modello di una pratica per un determinato servizio online offerto.

E' integrato nel frontend con un form builder per permettere alla redazione di creare i campi che servono.

Nomenclatura
------------

Modello Pratica = Content-Type che contiene il modello del form da compilare per l'utente.
Form = Elenco dei campi necessari per richiedere un determinato servizio online, definito nell'oggetto Modello Pratica. E' quello che i cittadini andranno a compilare per le richieste.
Pratica = Form compilato e salvato da parte dell'utente. Ogni Pratica ha un proprio codice identificativo che permetterà all'utente di consultarla e modificarla.

Salvataggio dati
================

Lo storage dei dati è basato su plone.souper, ma può essere facilmente sostituito con altri storage (ad esempio postgresql) semplicemente
registrando un adapter specifico.

Ogni volta che un utente compila il form, viene salvata una nuova entry in nello storage con i dati del form e una serie di dati accessori.


Restapi endpoints Pratica
=========================

Creazione nuova Pratica
-----------------------

Endpoint da chiamare sulla radice che accetta solamente chiamate in `POST`.

Solo gli utenti autenticati possono chiamare questo endpoint.

Campi obbligatori:

- **form**: Summary del modello pratica
- **data**: I dati compilati dall'utente.

Campi opzionali:

- **assigned_to**: Utente a cui è assegnata la Pratica.
- **state**: Stato di revisione della Pratica.

Gli unici stati possibili sono `draft` e `ongoing`. Vedi paragrafo dedicato agli stati, per maggiori informazioni.

Se lo stato è `draft`, i dati possono anche essere vuoti.

Ogni altro campo passato all'endpoint verrà scartato e non salvato nella Pratica.

Esempio::

    > curl -i -X POST http://nohost/plone/@pratica -H "Accept: application/json" -H "Content-Type: application/json" --data-raw '{"form_id": "xxx", "data": {...}}' --user admin:secret


Esempio di risposta (codice di risposta: `200``)::

    {"item_id": 123456}


Modifica Pratica
----------------

Endpoint da chiamare sulla radice del sito che accetta solamente chiamate in `PATCH`.

E' necessario passare anche il **item_id** di riferimento di una pratica.

Solo gli utenti autenticati possono chiamare questo endpoint.

Solamente gli utenti con un determinato permesso (*design.plone.iocittadino: Manage Pratica*) possono modificare le Pratiche create da altri utenti.

Campi:

- **data**: I dati compilati dall'utente (obbligatorio solamente per la pratica in stato draft o quando si fa il salvataggio finale).
- **assigned_to**: Utente a cui è assegnata la Pratica (non obbligatorio).
- **state**: Stato di revisione della Pratica (non obbligatorio).

Gli unici stati possibili sono `draft` e `ongoing`. Vedi paragrafo dedicato agli stati, per maggiori informazioni.

Non è possibile modificare una pratica dopo che va in stato `ongoing`.

Esempio::

    > curl -i -X PATCH http://nohost/plone/@pratica/123456 -H "Accept: application/json" -H "Content-Type: application/json" --data-raw '{"data": {...}}' --user admin:secret

Se la modifica ha esito positivo, il codice di risposta è `204` (OK senza dati).

Cancellazione Pratica
---------------------

Endpoint da chiamare sulla radice del sito che accetta chiamate in `DELETE`.

E' necessario passare anche il **item_id** di riferimento.

Solo gli utenti autenticati possono chiamare questo endpoint.

Solamente gli utenti con un determinato permesso (*design.plone.iocittadino: Manage Pratica*) possono cancellare le Pratiche create da altri utenti.

Esempio::

    > curl -i -X DELETE http://nohost/plone/@pratica/123456 -H "Accept: application/json" -H "Content-Type: application/json" --user admin:secret

Se la cancellazione ha esito positivo, il codice di risposta è `204` (OK senza dati).

Dettaglio Pratica
-----------------

Endpoint da chiamare sulla radice del sito che accetta chiamate in `GET`.

Se si passa un **item_id** di riferimento, ritorna i dati della pratica di riferimento.
Se non gli si passa nessun valore, allora vengono ritornati una serie di dati di default dell'utente per pre-popolare i campi del form.

Solo gli utenti autenticati possono chiamare questo endpoint.

Solamente gli utenti con un determinato permesso (*design.plone.iocittadino: Manage Pratica*) possono consultare le Pratiche create da altri utenti.

Esempio::

    > curl -i -X GET http://nohost/plone/@pratica/123456 -H "Accept: application/json" -H "Content-Type: application/json" --user admin:secret


Esempio di risposta senza parametri (codice di risposta: `200``)::

    {
        'data': {"email": "", "fullname": "", "id": "admin"},
    }


Esempio di risposta con parametri (codice di risposta: `200``)::

    {
        'creation_date': '2022-12-15T14:23:35',
        'data': { survey js form data in JSON fromat },
        'form': { ModelloPratica serialized to JSON summary},
        'item_id': 817407564,
        'state': 'foo',
        'userid': 'admin',
        'email': 'email'
        'next_steps': [{"days_number": "3", "title": "Presa in gestione"}],
        'assigned_to': 'pratica_manager'
        'has_report': true
        'servizi_collegati': ['<service uid>', '<service uid>'],
        'ufficio': { '<Uffico serialized to JSON summary>' },
        'messages': ['<Serialized to JSON Summary message>',]

    }


Di default nel campo `form` non viene ritornato lo schema, ma se serve, basta appendere alla request "show_schema=1"::

    > curl -i -X GET http://nohost/plone/@pratica/123456?show_schema=1 -H "Accept: application/json" -H "Content-Type: application/json" --user admin:secret

Elenco di Pratiche
------------------

Endpoint da chiamare sulla radice del sito che accetta chiamate in `GET`.

Ritorna una lista di pratiche filtrate in base ai parametri di ricerca passati.

Solo gli utenti autenticati possono chiamare questo endpoint.

Solamente gli utenti con un determinato permesso (*design.plone.iocittadino: Manage Pratica*) possono accedere alle Pratiche create da altri utenti.

Esempio p avere tutte le Pratiche (quindi senza nessun filtro)::

    > curl -i -X GET http://nohost/plone/@pratiche -H "Accept: application/json" -H "Content-Type: application/json" --user admin:secret

Esempio per avere solo le Pratiche di un singolo utente (quindi con un filtro impostato)::

    > curl -i -X GET http://nohost/plone/@pratiche?userid=foo -H "Accept: application/json" -H "Content-Type: application/json" --user admin:secret

Esempio di risposta (codice di risposta: `200``)::

    {
        "@id": "http://nohost/plone/@pratiche",
        "items": [
            {
                'creation_date': '2022-12-15T14:23:35',
                'data': { survey js form data in JSON fromat },
                'form': { ModelloPratica serialized to JSON summary},
                'item_id': 817407564,
                'state': 'foo',
                'userid': 'admin',
                'email': 'email'
                'next_steps': [{"days_number": "3", "title": "Presa in gestione"}],
                'assigned_to': 'pratica_manager'
                'has_report': true
                'servizi_collegati': ['<service uid>', '<service uid>'],
                'ufficio': { Uffico serialized to JSON summary }
                'messages': ['<Serialized to JSON Summary message>',]

            },
            {
                'creation_date': '2022-12-15T14:23:35',
                'data': { survey js form data in JSON fromat },
                'form': { ModelloPratica serialized to JSON summary},
                'item_id': 817407564,
                'state': 'foo',
                'userid': 'admin',
                'email': 'email'
                'next_steps': [{"days_number": "3", "title": "Presa in gestione"}],
                'assigned_to': 'pratica_manager'
                'has_report': true
                'servizi_collegati': ['<service uid>', '<service uid>'],
                'ufficio': { Uffico serialized to JSON summary },
                'messages': ['<Serialized to JSON Summary message>',]

            }
        ],
        "items_total": 2,
        "services": [
            ...
        ]
    }


Cambio stato pratica
--------------------

Endpoint da chiamare sulla radice del sito che accetta chiamate in `POST`.

E' necessario passare anche il **item_id** di riferimento nell'url.

Solo gli utenti autenticati possono chiamare questo endpoint.

Solamente gli utenti con un determinato permesso (*design.plone.iocittadino: Manage Pratica*) possono consultare le Pratiche create da altri utenti.

Esempio::

    > curl -i -X POST http://nohost/plone/@pratica-workflow/123456 -H "Accept: application/json" -H "Content-Type: application/json" --data-raw '{"state": "foo"}' --user admin:secret


Se il cambio di stato ha esito positivo, il codice di risposta è `204` (OK senza dati).


Stati della pratica
===================

E' stato creato un workflow semplificato per le Pratiche, per determinare lo stato di avanzamento dei lavori:

- Bozza (*draft*): stato iniziale quando l'utente dal form sceglie di salvare una bozza della Pratica che sta compilando, finché non è completata. Dallo stato **Bozza** è possibile andare allo stato **In corso**. Non è possibile ritornare allo stato bozza in nessun modo.
- In corso (*ongoing*): stato a cui si arriva dopo la bozza, o come stato iniziale quando l'utente compila il form senza passare per la bozza. Da questo stato, è possibile andare allo stato **Sospeso** o **Concluso**.
- Sospeso (*suspended*): stato in cui si richiede un'azione da parte dell'utente o dalla Pubblica Amministrazione. Da questo stato è possibile tornare indietro allo stato **In corso** o andare allo stato **Concluso**.
- Concluso (*completed*): stato finale della Pratica che ha completato l'iter di gestione. Una Pratica conclusa non può più cambiare stato.
- Annullato (*canceled*): stato finale della Pratica che è stata annullata. Una Pratica annullata non può più cambiare stato.

Restapi endpoints Messaggio
===========================

Creazione nuovo Messaggio
-------------------------

Endpoint da chiamare sulla radice che accetta solamente chiamate in `POST`.

Solo gli utenti autenticati possono chiamare questo endpoint.

Campi obbligatori:

- **pratica_id**: id della pratica legata.
- **message**: Il messaggio compilato dall'utente.

Campi opzionali:

- **state**: Stato di revisione del Messaggio.
- **notify_on_email**: Notifica l'utente che il messaggio è stato creato. Default: `true`

L'unico stato possibile `pending`. Vedi paragrafo dedicato agli stati, per maggiori informazioni.

Ogni altro campo passato all'endpoint verrà scartato e non salvato nel messaggio.

Esempio::

    > curl -i -X POST http://nohost/plone/@message -H "Accept: application/json" -H "Content-Type: application/json" --data-raw '{"pratica_id": "xxx", "message": "message"}' --user admin:secret


Esempio di risposta (codice di risposta: `200``)::

    {"item_id": 123456}

Esempio del messaggio con dei file allegati::
    > curl -i -X POST http://nohost/plone/@message -H "Accept: application/json" -H "Content-Type: application/json" --user admin:secret --data-raw
      '{
        "pratica_id": "xxx",
        "message": "message",
        "attachments": [{"filename": "Attacment.txt", "filestream": "b64 encoded file string"}]
        }'


Modifica Messaggio
------------------

Non implementato

Cancellazione Messaggio
-----------------------

Endpoint da chiamare sulla radice del sito che accetta chiamate in `DELETE`.

E' necessario passare anche il **item_id** di riferimento.

Solo gli utenti autenticati possono chiamare questo endpoint.

Solamente gli utenti con un determinato permesso (*design.plone.iocittadino: Manage Message*) possono cancellare i messaggi creati da altri utenti.

Esempio::

    > curl -i -X DELETE http://nohost/plone/@message/123456 -H "Accept: application/json" -H "Content-Type: application/json" --user admin:secret

Se la cancellazione ha esito positivo, il codice di risposta è `204` (OK senza dati).

Dettaglio Messaggio
-------------------

Endpoint da chiamare sulla radice del sito che accetta chiamate in `GET`.

E' necessario passare anche il **item_id** di riferimento.

Solo gli utenti autenticati possono chiamare questo endpoint.

Solamente gli utenti con un determinato permesso (*design.plone.iocittadino: Manage Message*) possono consultare i messaggi creati da altri utenti.

Esempio::

    > curl -i -X GET http://nohost/plone/@message/123456 -H "Accept: application/json" -H "Content-Type: application/json" --user admin:secret


Esempio di risposta (codice di risposta: `200``)::

    {
        'date': '2022-12-15T14:23:35',
        'message': 'a message',
        'pratica': { Related pratica serialized to JSON summary },
        'item_id': 817407564,
        'state': 'foo',
        'userid': 'admin',
        'attachments':
            [
                {
                    'filename': "attachment.txt",
                    'download_url': "http://nohost/plone/@message/123456/@@download/3d5e2b0e896a4607a2129c882eee73f0"
                },
                ...
            ]
    }

Elenco dei Messaggi
-------------------

Endpoint da chiamare sulla radice del sito che accetta chiamate in `GET`.

Ritorna una lista di pratiche filtrate in base ai parametri di ricerca passati.

Solo gli utenti autenticati possono chiamare questo endpoint.

Solamente gli utenti con un determinato permesso (*design.plone.iocittadino: Manage Message*) possono accedere ai messaggi create da altri utenti.

Esempio p avere tutti i Messaggi (quindi senza nessun filtro)::

    > curl -i -X GET http://nohost/plone/@messages -H "Accept: application/json" -H "Content-Type: application/json" --user admin:secret

Esempio per avere solo i messaggi di un singolo utente (quindi con un filtro impostato)::

    > curl -i -X GET http://nohost/plone/@messages?userid=foo -H "Accept: application/json" -H "Content-Type: application/json" --user admin:secret

Esempio di risposta (codice di risposta: `200``)::

    {
        "@id": "http://nohost/plone/@messages",
        "items": [
            {
                'date': '2022-12-15T14:23:35',
                'message': 'a message',
                'item_id': 817407564,
                'pratica': { Related pratica serialized to JSON summary },
                'state': 'foo',
                'userid': 'foo',
                'attachments':
                    [
                        {
                            'name': "attachment.txt",
                            'url': "http://nohost/plone/@message/123455/@@download/1/attachment.txt"
                        },
                        ...
                    ]
            },
            {
                'date': '2022-12-15T14:24:35',
                'message': 'a mssage',
                'item_id': 817407564,
                'pratica': { Related pratica serialized to JSON summary },
                'state': 'foo',
                'userid': 'foo',
                'attachments':
                [
                    {
                        'name': "attachment.txt",
                        'url': "http://nohost/plone/@message/123456/@@download/1/attachment.txt"
                    },
                    ...
                ]
            }
        ],
        "items_total": 2,
    }


Cambio stato Messaggio
----------------------

Endpoint da chiamare sulla radice del sito che accetta chiamate in `GET`.

E' necessario passare anche il **item_id** di riferimento.

Solo gli utenti autenticati possono chiamare questo endpoint.

Solamente gli utenti con un determinato permesso (*design.plone.iocittadino: Manage Message*) possono consultare i Messaggi create da altri utenti.

Esempio::

    > curl -i -X POST http://nohost/plone/@message-workflow/123456 -H "Accept: application/json" -H "Content-Type: application/json" --data-raw '{"state": "foo"}' --user admin:secret


Se il cambio di stato ha esito positivo, il codice di risposta è `204` (OK senza dati).


Stati del Messaggio
===================

E' stato creato un workflow semplificato per le Pratiche, per determinare lo stato di avanzamento dei lavori:

- Creato (*pending*): stato iniziale quando il messaggio è stato creato **Inviato**
- Inviato (*sent*): stato indica che il messaggio è stato inviato **Visualizzato**
- Visualizzato (*seen*): stato finale dopo che il messaggio è stato visualizzato al cliente

Operatori pratiche
==================

In fase di installazione, viene creato un nuovo gruppo "*Operatori pratiche*" in cui andranno inseriti gli utenti che
si occuperanno della gestione delle pratiche.

Questo gruppo ha un permesso speciale "*Gestore Pratiche*" che gli permette di gestire le pratiche appunto.

@operatori_pratica endpoint
---------------------------

Endpoint per permettere di avere la lista degli utenti inseriti nel gruppo (senza avere i permessi di leggere i membri dei gruppi Plone).

Esempio di chiamata::

    > curl -i -X GET http://localhost:8080/Plone/++api++/@operatori_pratica --user admin:secret

E la risposta è qualcosa del genere::

    {
        "@id": "http://localhost:8080/Plone/@groups/operatori_pratiche",
        "items": [
            {
                "label": "John Doe",
                "value": "jdoe"
            }
        ],
        "items_total": 1
    }

Estensione della pratica
========================
Tramite un sistema di utility è possibile estendere sia i field della pratica che
i campi tornati nel serializer della pratica.

Per estendere i field della pratica è necessario registrare un'utility tipo::

    @interface.implementer(IPraticaStoreFieldsExtender)
    class FieldExtender(object):
        @property
        def fields(self):
            return {
                "new_field_a": {"required": False},
                "new_field_b": {"required": False},
                "new_field_c": {"required": False},
            }

Per estendere il serializer è necessario registrare un'utility tipo::

    @interface.implementer(IPraticaStoreSerializerExtender)
    class ExtendsPraticaSerializer(object):
        def get_fields(self, pratica):
            return {
                "new_field_a": "A_value",
                "new_field_b": "B_value",
                "new_field_c": "C_value",
            }

La stessa identica cosa è possibile per i messaggi, registrando utility fatte
alla stessa identica maniera per le interfacce IMessageStoreFieldsExtender e
IMessageStoreSerializerExtender


Traduzioni
==========

Questo prodotto è stato tradotto in:

- Inglese
- Italiano

Report PDF
==========

E' possibile reperire il report della pratica in pdf chiamando la vista **@@pratica_report** sulla radice del sito.

Parametri::

    - **item_id**: l'id della pratica

Solo gli utenti autenticati possono chiamare questa vista.

Solamente gli utenti con un determinato permesso (*design.plone.iocittadino: Manage Pratica*) possono consultare le pratiche create da altri utenti.


Installazione
=============

Per installare design.plone.iocittadino basta aggiungere il prodotto nel buildout::

    [buildout]

    ...

    eggs =
        design.plone.iocittadino


e poi eseguire il comando ``bin/buildout``.

Il prodotto va poi installato da pannello di controllo.

Il prodotto richiede installazione del pacchetto `wkhtmltopdff`

Autori
======

Questo prodotto è stato sviluppato da RedTurtle Technology.

.. image:: http://www.redturtle.net/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.net/


Licenza
-------

Questo prodotto è sotto la licenza GPLv2.
