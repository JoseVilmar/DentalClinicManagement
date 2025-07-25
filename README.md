Overview:

The Dental Clinic Management Project is a comprehensive web application designed to streamline and enhance the administrative and operational aspects of a dental clinic. This project leverages the robust capabilities of HTML, CSS, and Django to provide a seamless user experience for both clinic staff and patients.


Technologies Used:

HTML: Provides the structural framework for the web pages, ensuring content is organized and accessible.

CSS: Adds styling to the HTML elements, creating a visually appealing and user-friendly interface.

Django: A high-level Python web framework that handles the backend functionality, including database interactions, authentication, and dynamic content rendering.




Key Features:

Patient Management

Registration and Profile Management: Patients can easily register, update their profiles, and manage their personal information.

Appointment Scheduling: Allows patients to book, reschedule, or cancel appointments with dentists. The system provides real-time availability to avoid double bookings.



Staff Management:

Staff Scheduling: Enables efficient scheduling of dentist shifts and availability, ensuring optimal resource utilization.



Appointment and Treatment Management:

Appointment Tracking: Keeps track of all upcoming, and completed appointments with detailed records.

Treatment Records: Maintains comprehensive treatment history for each patient, including diagnosis, treatment plans, and follow-up care.



Billing and Payments:

Payment Processing: Integrates with payment gateways to facilitate secure and convenient payment options for patients.



User Interface:

The project features a responsive and intuitive user interface designed using HTML and CSS. The interface ensures a smooth navigation experience across different devices, including desktops, tablets, and mobile phones.



Benefits:

Efficiency: Automates and streamlines various administrative tasks, reducing the workload on clinic staff.

Accessibility: Provides patients with easy access to their records and appointment schedules.

Accuracy: Minimizes errors in scheduling, billing, and patient records through automated processes.

Scalability: Built on Django, the project can be easily scaled to accommodate the growing needs of a dental clinic.

---

## Setup Instructions

### 1. Clone o repositório
```bash
git clone https://github.com/JoseVilmar/DentalClinicManagement.git
cd DentalClinicManagement
```

### 2. Crie o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure o arquivo `.env`
Crie um arquivo `.env` na raiz do projeto (mesmo nível do `manage.py`) com o seguinte conteúdo:

```
DB_NAME=dentalmanagement
DB_USER=root
DB_PASSWORD=7499373180
DB_HOST=127.0.0.1
DB_PORT=3306
EMAIL_HOST_PASSWORD=fzwlpnlqruhaarxc
```

> ⚠️ Se você estiver usando MAMP, altere `DB_HOST=localhost` e `DB_PORT=8889`

### 5. Rode o projeto
```bash
python manage.py runserver
```

Acesse `http://127.0.0.1:8000/` no navegador.

---
