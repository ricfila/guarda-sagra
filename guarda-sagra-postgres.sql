CREATE TABLE IF NOT EXISTS "aree" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "nome" varchar(32),
  "coperto" numeric(10, 2),
  "asporto" numeric(10, 2),
  PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS "tipologie" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "nome" varchar(64),
  "posizione" int,
  "sfondo" varchar(16) DEFAULT NULL,
  "visibile" boolean,
  PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS "articoli" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "nome" varchar(64),
  "nome_breve" varchar(32),
  "prezzo" numeric(10, 2),
  "copia_cliente" boolean,
  "copia_cucina" boolean,
  "copia_bar" boolean,
  "copia_pizzeria" boolean,
  "copia_rosticceria" boolean,
  PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS "ingredienti" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "nome" varchar(64),
  "nome_breve" varchar(32),
  "settore" varchar(16),
  "visibile" boolean,
  PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS "articoli_ingredienti" (
  "articolo" int NOT NULL,
  "ingrediente" int NOT NULL,
  "quantita_massima" numeric(10, 2),
  "obbligatorio" boolean,
  "sovrapprezzo" numeric(10, 2),
  "sfondo" varchar(16) DEFAULT NULL,
  "posizione" int,
  "visibile" boolean,
  PRIMARY KEY ("articolo", "ingrediente"),
  FOREIGN KEY ("articolo") REFERENCES "articoli" ("id"),
  FOREIGN KEY ("ingrediente") REFERENCES "ingredienti" ("id")
);
CREATE TABLE IF NOT EXISTS "listini" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "nome" varchar(64),
  PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS "articoli_listini" (
  "articolo" int NOT NULL,
  "listino" int NOT NULL,
  "tipologia" int,
  "posizione" int,
  "sfondo" varchar(16) DEFAULT NULL,
  "visibile" boolean,
  PRIMARY KEY ("articolo", "listino"),
  FOREIGN KEY ("articolo") REFERENCES "articoli" ("id"),
  FOREIGN KEY ("listino") REFERENCES "listini" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY ("tipologia") REFERENCES "tipologie" ("id") ON DELETE SET NULL ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "profili" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "nome" varchar(16),
  "privilegi" int,
  "area" int DEFAULT NULL,
  "password" varchar(128),
  "arrotonda" numeric(4, 2) DEFAULT NULL,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("area") REFERENCES "aree" ("id")
);
CREATE TABLE IF NOT EXISTS "casse_listini" (
  "cassa" int NOT NULL,
  "listino" int NOT NULL,
  "data_inizio" date,
  "data_fine" date,
  PRIMARY KEY ("cassa", "listino"),
  FOREIGN KEY ("cassa") REFERENCES "profili" ("id"),
  FOREIGN KEY ("listino") REFERENCES "listini" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "tipi_pagamento" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "nome" varchar(16),
  "posizione" int,
  "visibile" boolean,
  PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS "ordini" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "progressivo" int,
  "data" date,
  "ora" time,
  "cliente" varchar(64),
  "coperti" int,
  "tavolo" varchar(32),
  "totale" numeric(10, 2),
  "note" varchar(128),
  "cassa" int NOT NULL,
  "tipo_pagamento" int NOT NULL,
  "menu_omaggio" boolean,
  "per_operatori" boolean,
  "preordine" boolean,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("cassa") REFERENCES "profili" ("id"),
  FOREIGN KEY ("tipo_pagamento") REFERENCES "tipi_pagamento" ("id") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "stati" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "copia" int,
  "posizione" int,
  "nome" varchar(16),
  "attesaTavolo" boolean,
  PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS "passaggi_stato" (
  "ordine" int NOT NULL,
  "stato" int NOT NULL,
  "ora" time,
  "agente" varchar(32),
  PRIMARY KEY ("ordine", "stato"),
  FOREIGN KEY ("ordine") REFERENCES "ordini" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY ("stato") REFERENCES "stati" ("id")
);
CREATE TABLE IF NOT EXISTS "righe_articoli" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "ordine" int NOT NULL,
  "articolo" int NOT NULL,
  "quantita" int,
  "note" varchar(128),
  PRIMARY KEY ("id"),
  FOREIGN KEY ("ordine") REFERENCES "ordini" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY ("articolo") REFERENCES "articoli" ("id")
);
CREATE TABLE IF NOT EXISTS "righe_ingredienti" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "riga_articolo" int NOT NULL,
  "ingrediente" int NOT NULL,
  "quantita" int,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("riga_articolo") REFERENCES "righe_articoli" ("id"),
  FOREIGN KEY ("ingrediente") REFERENCES "ingredienti" ("id")
);
CREATE TABLE IF NOT EXISTS "sconti" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "nome" varchar(64),
  "nome_breve" varchar(32),
  "valore" numeric(10, 2),
  "da_numero" numeric(10),
  "a_numero" numeric(10),
  "percentuale" boolean,
  PRIMARY KEY ("id")
);
CREATE TABLE IF NOT EXISTS "righe_sconti" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "ordine" int NOT NULL,
  "sconto" int NOT NULL,
  "numero_buono" int,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("ordine") REFERENCES "ordini" ("id") ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY ("sconto") REFERENCES "sconti" ("id")
);
CREATE TABLE IF NOT EXISTS "sconti_listini" (
  "sconto" int NOT NULL,
  "listino" int NOT NULL,
  "posizione" int,
  "visibile" boolean,
  PRIMARY KEY ("sconto", "listino"),
  FOREIGN KEY ("sconto") REFERENCES "sconti" ("id"),
  FOREIGN KEY ("listino") REFERENCES "listini" ("id") ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "scorte" (
  "id" int GENERATED BY DEFAULT AS IDENTITY NOT NULL,
  "ingrediente" int,
  "scorta" numeric(10, 2),
  "data_ora" timestamp,
  "attuale" boolean,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("ingrediente") REFERENCES "ingredienti" ("id")
);