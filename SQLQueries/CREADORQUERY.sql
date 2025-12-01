CREATE DATABASE AgroMon;
GO
USE AgroMon;
GO

--***************************************************--
-- CREADOR PARCELAS

CREATE TABLE Parcelas (
    idParcela INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(150) NOT NULL,
    tipoCultivo VARCHAR(80) NOT NULL,
    area FLOAT NOT NULL,
    profundidadRaiz FLOAT NULL,
    eficienciaRiego FLOAT NULL,
    umbralHumedadMin FLOAT NULL,
    umbralHumedadMax FLOAT NULL,
    volumenDeseado FLOAT NULL
);
GO

--***************************************************--
-- CREADOR SENSORES

CREATE TABLE Sensores (
    idSensor INT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    idParcela INT NOT NULL,
    estado VARCHAR(50),
    ubicacionParcela VARCHAR(150),
    unidadMedida VARCHAR(50),
    rangoValido VARCHAR(50),

    FOREIGN KEY (idParcela) REFERENCES Parcelas(idParcela)
        ON DELETE CASCADE
);
GO

--***************************************************--
-- CREADOR CALCULO VOLUMEN RIEGO

CREATE TABLE CalculoVolumenRiego (
    idCalculo INT IDENTITY PRIMARY KEY,
    idParcela INT NOT NULL,
    fecha DATE NOT NULL,
    volumenRiego FLOAT NOT NULL,

    FOREIGN KEY (idParcela) REFERENCES Parcelas(idParcela)
);
GO
