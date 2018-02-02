CREATE TABLE empleado
(
  empleado_oid integer NOT NULL DEFAULT nextval('empleado_empleado_oid'::regclass),
  cedula text NOT NULL,
  primer_nombre text,
  segundo_nombre text,
  primer_apellido text,
  segundo_apellido text,
  nombre_completo text,
  fecha_nacimiento timestamp without time zone,
  edad integer,
  numero_aportaciones integer,
  direccion1 text,
  direccion2 text,
  telefono1 text,
  telefono2 text,
  email text,
  sueldo double precision,
  dias_laborales integer,
  sexo_oid integer,
  genero_oid integer,
  nivel_academico_oid integer,
  estado_civil_oid integer,
  foto bytea,
  banco_id integer,
  numero_cuenta_bancaria text,
  tipo_discapacidad_oid integer,
  discapacidad_descripcion text,
  nombre_recomendado text,
  telefono_recomendado text,
  celular_recomendado text,
  ciudad_oid integer,
  es_discapacitado boolean DEFAULT false,
  es_activo boolean DEFAULT false,
  es_carga_familiar boolean DEFAULT false,
  CONSTRAINT "PK_dbo.Empleado" PRIMARY KEY (empleado_oid),
  CONSTRAINT "FK_dbo.Empleado_dbo.Banco_bancoId" FOREIGN KEY (banco_id)
      REFERENCES banco (banco_oid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "FK_dbo.Empleado_dbo.Ciudads_CiudadOid" FOREIGN KEY (ciudad_oid)
      REFERENCES ciudad (ciudad_oid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "FK_dbo.Empleado_dbo.EstadoCivil_EstadoCivilOid" FOREIGN KEY (estado_civil_oid)
      REFERENCES estado_civil (estado_civil_oid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "FK_dbo.Empleado_dbo.Genero_GeneroOid" FOREIGN KEY (genero_oid)
      REFERENCES genero (genero_oid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "FK_dbo.Empleado_dbo.NivelAcademico_NivelAcademicoOid" FOREIGN KEY (nivel_academico_oid)
      REFERENCES nivel_academico (nivel_academico_oid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "FK_dbo.Empleado_dbo.Sexo_SexoOid" FOREIGN KEY (sexo_oid)
      REFERENCES sexo (sexo_oid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "FK_dbo.Empleado_dbo.TipoDiscapacidad_tipoDiscapacidad" FOREIGN KEY (tipo_discapacidad_oid)
      REFERENCES tipo_discapacidad (tipo_discapacidad_oid) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE empleado
  OWNER TO postgres;
  
  
  CREATE TABLE sexo
(
  sexo_oid integer NOT NULL DEFAULT nextval('sexo_sexo_oid'::regclass),
  descripcion text,
  CONSTRAINT "PK_dbo.Sexo" PRIMARY KEY (sexo_oid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE sexo
  OWNER TO postgres;
  
  
  
  CREATE TABLE genero
(
  genero_oid integer NOT NULL DEFAULT nextval('genero_genero_oid'::regclass),
  descripcion text,
  CONSTRAINT "PK_dbo.Genero" PRIMARY KEY (genero_oid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE genero
  OWNER TO postgres;
  
  
  CREATE TABLE nivel_academico
(
  nivel_academico_oid integer NOT NULL DEFAULT nextval('nivel_academico_nivel_academico_oid'::regclass),
  descripcion text,
  CONSTRAINT "PK_dbo.NivelAcademico" PRIMARY KEY (nivel_academico_oid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE nivel_academico
  OWNER TO postgres;
  
  
  CREATE TABLE estado_civil
(
  estado_civil_oid integer NOT NULL DEFAULT nextval('estado_civil_estado_civil_oid'::regclass),
  descripcion text,
  CONSTRAINT "PK_dbo.EstadoCivil" PRIMARY KEY (estado_civil_oid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE estado_civil
  OWNER TO postgres;

  
  
  CREATE TABLE banco
(
  banco_oid integer NOT NULL DEFAULT nextval('banco_banco_oid'::regclass),
  descripcion text,
  codigo_banco text,
  CONSTRAINT "PK_dbo.Banco" PRIMARY KEY (banco_oid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE banco
  OWNER TO postgres;

  
  CREATE TABLE tipo_discapacidad
(
  tipo_discapacidad_oid integer NOT NULL DEFAULT nextval('tipo_discapacidad_tipo_discapacidad_oid'::regclass),
  descripcion text,
  CONSTRAINT "PK_dbo.TipoDiscapacidad" PRIMARY KEY (tipo_discapacidad_oid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tipo_discapacidad
  OWNER TO postgres;
