CREATE TABLE Caregivers (
    Username VARCHAR(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Patients (
    Username VARCHAR(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time DATE,
    Username VARCHAR(255) REFERENCES Caregivers,
    booked INT,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name VARCHAR(255),
    Doses INT,
    PRIMARY KEY (Name)
);

CREATE TABLE Appointments (
    AppointmentID VARCHAR(255),
    Vaccine VARCHAR(255),
    Time DATE,
    Caregiver VARCHAR(255),
    Patient VARCHAR(255),
    FOREIGN KEY (Vaccine) REFERENCES Vaccines(Name),
    FOREIGN KEY (Caregiver) REFERENCES Caregivers(Username),
    FOREIGN KEY (Patient) REFERENCES Patients(Username),
    PRIMARY KEY (AppointmentID)
);