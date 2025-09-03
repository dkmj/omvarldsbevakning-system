Below is a detailed blueprint for building your web‑based omvärldsbevakning system along with iterative, test-driven code-generation prompts. We start with a high‑level plan that breaks the project into major modules, then decompose each module into small, manageable, and interrelated steps. Each prompt builds on the previous one to ensure incremental progress, robust testing, and smooth integration.

High‑Level Blueprint
	1.	Project Structure & Architecture
	•	Frontend: Interfaces for login, observation submission, admin moderation, clustering, search, and report download.
	•	Backend: REST API endpoints for users, observations, file handling, clustering, reporting, search, and logging.
	•	Database & Storage: Separate storage for user data, observation metadata, logs, and a file system or cloud solution for attachments.
	•	Authentication & Roles: Role‑based access for Experts (Bidragare), Database Administrators (Databasadministratörer), and Superadministrators.
	•	Testing & Integration: Use test‑driven development at every stage to validate functionality and data flow.
	2.	Major Modules & User Flows
	•	User Management: Registration, login, and role verification.
	•	Observation Submission: CRUD operations for observations including file uploads (PDF, text, images up to 25MB) and tags.
	•	File Upload Handling: Validate file type/size and integrate with storage.
	•	Admin Moderation: Interface for admins to mark observations as “Approved”, “Uncertain”, or “Deletion.”
	•	Clustering Module: Collaborative interface for color‑coding observations into clusters (with manual naming, motivation, and robustness scoring).
	•	Report Generation: Compile approved observations and clusters into a final, locked PDF report.
	•	Search & Filtering: Query observations by title, description, tags, and date filters.
	•	Logging & Backup: Record user actions and enable data recovery through backups.
	3.	Incremental and Test‑Driven Development
	•	Begin with a minimal project skeleton.
	•	Add modules one at a time with dedicated API endpoints and UI components.
	•	Write unit and integration tests as you go.
	•	Wire the modules together so that every new feature integrates with previous work.

Below are a series of markdown‑formatted prompts (each in a separate code block tagged as text) that you can feed to a code‑generation LLM to implement the project step by step.

Prompt 1: Project Setup and User Authentication
-------------------------------------------------
Set up a new web-based project using your preferred backend and frontend frameworks. Create a basic project skeleton that includes:
- A user management system with role‑based access control for three roles: Expert (Bidragare), Admin (Databasadministratör), and Superadmin.
- Endpoints for user registration, login, and role validation.
- A simple UI for login and registration.
- Unit tests for user creation, authentication, and role access.
Ensure that the code is modular and well‑documented to support future extensions.

Prompt 2: Observation Submission Module
-----------------------------------------
Develop the Observation Submission module with the following requirements:
- Create a REST API endpoint that allows an authenticated expert to submit an observation with these fields:
  • Auto‑filled date.
  • Expert ID (from the logged‑in user).
  • Title.
  • Link or file upload (supporting PDFs, text files, or images up to 25MB).
  • “Why interesting?” field (20–500 characters).
  • Optional tags.
- Build a simple UI form for submitting observations and for listing previously submitted entries by the same user.
- Write tests to verify that only authenticated users can submit and edit their own observations.

Prompt 3: File Upload Handling
--------------------------------
Enhance the Observation Submission module by implementing robust file upload functionality:
- Validate uploaded files to ensure they are of acceptable types (PDF, text, image) and do not exceed 25MB.
- Integrate file storage with the observation database by saving file metadata and references.
- Ensure error handling for invalid files.
- Write tests that check for file type and size validation and confirm that valid files are stored and retrievable.

Prompt 4: Admin Moderation Interface
--------------------------------------
Develop the Admin Moderation module:
- Create secure API endpoints and a UI interface for database administrators to view all submitted observations.
- Enable admins to mark each observation with a status: “Approved”, “Uncertain”, or “Deletion.”
- Provide filtering and search options within the admin interface.
- Write tests to ensure that only admins can perform moderation actions and that status changes are correctly recorded.

Prompt 5: Clustering Module for Observation Grouping
------------------------------------------------------
Create a Clustering module to support collaborative clustering during review meetings:
- Develop an interface that displays all approved observations in a scrollable list.
- Allow admins to assign color codes to observations to group them into clusters.
- Enable observations to belong to multiple clusters if needed.
- Include features for manual naming, adding a brief motivation, and assigning a robustness score (0–100) to each cluster.
- Implement an auto-sync mechanism (e.g., updating every 15–30 seconds) for collaborative work.
- Write tests to verify that clustering actions update the database correctly and that the UI reflects cluster assignments accurately.

Prompt 6: Report Generation Module
-------------------------------------
Build the Report Generation module to compile the final output:
- Create an API endpoint that generates a locked report (PDF or equivalent) containing:
  • Cluster names, descriptions, and robustness scores.
  • All approved observations organized by cluster.
- Include a download link in the UI for users to access historical reports.
- Write tests to ensure the generated report includes all required information and follows the specified format.

Prompt 7: Search and Filtering Functionality
----------------------------------------------
Implement a Search and Filtering module:
- Develop a search API that lets users query observations by title, description, tags, and date ranges.
- Build a UI component for entering search queries and selecting filters.
- Ensure that the search results update dynamically and accurately reflect the database contents.
- Write tests to validate that search queries return the correct results and that filtering functions properly.

Prompt 8: Logging and Activity History
----------------------------------------
Develop the Logging and Activity History module:
- Implement an activity log that records every user action (login, observation submission, deletion, moderation, clustering, report generation) along with timestamps and user IDs.
- Create an admin interface for viewing and filtering these logs.
- Set up periodic database backups for data safety.
- Write tests to confirm that every significant action generates a log entry and that the logs can be queried reliably.

Prompt 9: System Integration and End-to-End Testing
-----------------------------------------------------
Integrate all modules—User Management, Observation Submission, File Upload, Admin Moderation, Clustering, Report Generation, Search, and Logging—into a unified system:
- Ensure seamless navigation and data flow between modules.
- Wire the UI components with the corresponding API endpoints.
- Remove any orphaned code by confirming that every new feature is integrated with existing functionality.
- Write comprehensive end-to-end tests simulating complete user flows, from observation submission by an expert, through moderation and clustering by admins, to final report generation and download.

This series of prompts provides a solid foundation for a code-generation LLM to implement the system in a test-driven manner, ensuring best practices and incremental progress. Each prompt builds upon the previous ones and finishes with wiring together the various components. Happy coding, and yay for steady progress!