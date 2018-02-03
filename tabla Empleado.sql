create table EMPLEADO (
   EMPLEADO_OID         SERIAL               not null,
   CEDULA               TEXT                 null,
   NOMBRES              TEXT                 null,
   APELLIDOS            TEXT                 null,
   FECHA_NACIMIENTO     TEXT                null,
   EDAD                 INT4                 null,
   NUMERO_APORTACIONES  INT4                 null,
   DIRECCION1           TEXT                 null,
   DIRECCION2           TEXT                 null,
   TELEFONO1            TEXT                 null,
   TELEFONO2            TEXT                 null,
   EMAIL                TEXT                 null,
   SUELDO               DECIMAL(6,2)         null,
   DIAS_LABORALES       INT4                 null,
   GENERO               TEXT                 null,
   NIVEL_ACADEMICO      TEXT                 null,
   NUMERO_CUENTA_BANCARIA TEXT                 null,
   TIPO_DISCAPACIDAD    TEXT                null,
   NOMBRE_RECOMENDADO   TEXT                 null,
   TELEFONO_RECOMENDADO TEXT                 null,
   CELULAR_RECOMENDADO  TEXT                 null,
   CIUDAD               TEXT                 null,
   FOTO                 TEXT            null,
   constraint PK_EMPLEADO primary key (EMPLEADO_OID)
);

insert into empleado (cedula, nombres) values (5435, 'o')

drop table empleado;
select * from empleado