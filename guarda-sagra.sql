
CREATE TABLE "aree" (
  "id" INTEGER NOT NULL,
  "nome" CHARACTER VARYING(32),
  "coperto" NUMERIC(10, 2),
  "asporto" NUMERIC(10, 2),
  PRIMARY KEY ("id")
);

CREATE TABLE "articoli" (
  "id" INTEGER NOT NULL,
  "nome" CHARACTER VARYING(64),
  "nome_breve" CHARACTER VARYING(32),
  "tipologia" INTEGER NOT NULL,
  "prezzo" NUMERIC(10, 2),
  "copia_cliente" BOOLEAN,
  "copia_cucina" BOOLEAN,
  "copia_bar" BOOLEAN,
  "copia_pizzeria" BOOLEAN,
  "copia_rosticceria" BOOLEAN,
  PRIMARY KEY ("id")
);

CREATE TABLE "articoli_ingredienti" (
  "articolo" INTEGER NOT NULL,
  "ingrediente" INTEGER NOT NULL,
  "quantita_massima" NUMERIC(10, 2),
  "obbligatorio" BOOLEAN,
  "sovrapprezzo" NUMERIC(10, 2),
  "sfondo" INTEGER,
  "posizione" INTEGER,
  "visibile" BOOLEAN,
  PRIMARY KEY ("articolo", "ingrediente")
);

CREATE TABLE "articoli_listini" (
  "articolo" INTEGER NOT NULL,
  "listino" INTEGER NOT NULL,
  "posizione" INTEGER,
  "sfondo" INTEGER,
  "visibile" BOOLEAN,
  PRIMARY KEY ("articolo", "listino")
);

CREATE TABLE "casse_listini" (
  "cassa" INTEGER NOT NULL,
  "listino" INTEGER NOT NULL,
  "data_inizio" DATE,
  "data_fine" DATE,
  PRIMARY KEY ("cassa", "listino")
);

CREATE TABLE "ingredienti" (
  "id" INTEGER NOT NULL,
  "nome" CHARACTER VARYING(64),
  "nome_breve" CHARACTER VARYING(32),
  "settore" CHARACTER VARYING(16),
  "visibile" BOOLEAN,
  PRIMARY KEY ("id")
);

CREATE TABLE "listini" (
  "id" INTEGER NOT NULL,
  "nome" CHARACTER VARYING(64),
  PRIMARY KEY ("id")
);

CREATE TABLE "ordini" (
  "id" INTEGER NOT NULL,
  "progressivo" INTEGER,
  "data" DATE,
  "ora" TIME,
  "cliente" CHARACTER VARYING(64),
  "coperti" INTEGER,
  "tavolo" CHARACTER VARYING(32),
  "totale" NUMERIC(10, 2),
  "note" CHARACTER VARYING(128),
  "cassa" INTEGER NOT NULL,
  "tipo_pagamento" INTEGER NOT NULL,
  "menu_omaggio" BOOLEAN,
  "per_operatori" BOOLEAN,
  "preordine" BOOLEAN,
  PRIMARY KEY ("id")
);

CREATE TABLE "passaggi_stato" (
  "ordine" INTEGER NOT NULL,
  "stato" INTEGER NOT NULL,
  "ora" TIME,
  "agente" CHARACTER VARYING(32),
  PRIMARY KEY ("ordine", "stato")
);

CREATE TABLE "profili" (
  "id" INTEGER NOT NULL,
  "nome" CHARACTER VARYING(16),
  "admin" INTEGER,
  "area" INTEGER,
  "password" CHARACTER VARYING(128),
  "arrotonda" NUMERIC(4,2),
  PRIMARY KEY ("id")
);

CREATE TABLE "righe_articoli" (
  "id" INTEGER NOT NULL,
  "ordine" INTEGER NOT NULL,
  "articolo" INTEGER NOT NULL,
  "quantita" INTEGER,
  "note" CHARACTER VARYING(128),
  PRIMARY KEY ("id")
);

CREATE TABLE "righe_ingredienti" (
  "id" INTEGER NOT NULL,
  "riga_articolo" INTEGER NOT NULL,
  "ingrediente" INTEGER NOT NULL,
  "quantita" INTEGER,
  PRIMARY KEY ("id")
);

CREATE TABLE "righe_sconto" (
  "id" INTEGER NOT NULL,
  "ordine" INTEGER NOT NULL,
  "sconto" INTEGER NOT NULL,
  "numero_buono" INTEGER,
  PRIMARY KEY ("id")
);

CREATE TABLE "sconti" (
  "id" INTEGER NOT NULL,
  "nome" CHARACTER VARYING(64),
  "nome_breve" CHARACTER VARYING(32),
  "valore" NUMERIC(10, 2),
  "da_numero" NUMERIC(10, 0),
  "a_numero" NUMERIC(10, 0),
  "percentuale" BOOLEAN,
  PRIMARY KEY ("id")
);

CREATE TABLE "sconti_listini" (
  "sconto" INTEGER NOT NULL,
  "listino" INTEGER NOT NULL,
  "posizione" INTEGER,
  "visibile" BOOLEAN,
  PRIMARY KEY ("sconto", "listino")
);

CREATE TABLE "scorte" (
  "id" INTEGER NOT NULL,
  "ingrediente" INTEGER,
  "scorta" NUMERIC(10,2),
  "data_ora" TIMESTAMP,
  "attuale" BOOLEAN,
  PRIMARY KEY ("id")
);

CREATE TABLE "stati" (
  "id" INTEGER NOT NULL,
  "copia" INTEGER,
  "posizione" INTEGER,
  "nome" CHARACTER VARYING(16),
  "attesaTavolo" BOOLEAN,
  --"tipologia" INTEGER, --meglio un collegamento N-N
  PRIMARY KEY ("id")
);

CREATE TABLE "tipi_pagamento" (
  "id" INTEGER NOT NULL,
  "nome" CHARACTER VARYING(16),
  "posizione" INTEGER,
  "visibile" BOOLEAN,
  PRIMARY KEY ("id")
);

CREATE TABLE "tipologie" (
  "id" INTEGER NOT NULL,
  "nome" CHARACTER VARYING(64),
  "posizione" INTEGER,
  "sfondo" INTEGER,
  "visibile" BOOLEAN,
  PRIMARY KEY ("id")
);

ALTER TABLE "articoli" ADD FOREIGN KEY ("tipologia") REFERENCES "tipologie" ("id");

ALTER TABLE "articoli_ingredienti" ADD FOREIGN KEY ("articolo") REFERENCES "articoli" ("id");
ALTER TABLE "articoli_ingredienti" ADD FOREIGN KEY ("ingrediente") REFERENCES "ingredienti" ("id");

ALTER TABLE "articoli_listini" ADD FOREIGN KEY ("articolo") REFERENCES "articoli" ("id");
ALTER TABLE "articoli_listini" ADD FOREIGN KEY ("listino") REFERENCES "listini" ("id") ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE "profili" ADD FOREIGN KEY ("area") REFERENCES "aree" ("id");

ALTER TABLE "casse_listini" ADD FOREIGN KEY ("cassa") REFERENCES "profili" ("id");
ALTER TABLE "casse_listini" ADD FOREIGN KEY ("listino") REFERENCES "listini" ("id") ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE "ordini" ADD FOREIGN KEY ("cassa") REFERENCES "profili" ("id");
ALTER TABLE "ordini" ADD FOREIGN KEY ("tipo_pagamento") REFERENCES "tipi_pagamento" ("id") ON UPDATE CASCADE;

ALTER TABLE "passaggi_stato" ADD FOREIGN KEY ("ordine") REFERENCES "ordini" ("id") ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "passaggi_stato" ADD FOREIGN KEY ("stato") REFERENCES "stati" ("id");

ALTER TABLE "righe_articoli" ADD FOREIGN KEY ("ordine") REFERENCES "ordini" ("id") ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "righe_articoli" ADD FOREIGN KEY ("articolo") REFERENCES "articoli" ("id");

ALTER TABLE "righe_ingredienti" ADD FOREIGN KEY ("riga_articolo") REFERENCES "righe_articoli" ("id");
ALTER TABLE "righe_ingredienti" ADD FOREIGN KEY ("ingrediente") REFERENCES "ingredienti" ("id");

ALTER TABLE "righe_sconto" ADD FOREIGN KEY ("ordine") REFERENCES "ordini" ("id") ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE "righe_sconto" ADD FOREIGN KEY ("sconto") REFERENCES "sconti" ("id");

ALTER TABLE "sconti_listini" ADD FOREIGN KEY ("sconto") REFERENCES "sconti" ("id");
ALTER TABLE "sconti_listini" ADD FOREIGN KEY ("listino") REFERENCES "listini" ("id") ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE "scorte" ADD FOREIGN KEY ("ingrediente") REFERENCES "ingredienti" ("id");
