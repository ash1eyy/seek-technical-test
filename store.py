from datetime import datetime, timezone


class Store:
    def __init__(self):
        self.jobs = []
        self.applications = []
        self._next_job_id = 1
        self._next_application_id = 1

    def add_job(self, title, description, location):
        job = {
            "id": self._next_job_id,
            "title": title,
            "description": description,
            "location": location,
            "created_at": datetime.now(timezone.utc),
            "status": "OPEN",
        }

        self._next_job_id += 1
        self.jobs.append(job)

        return job

    def get_job(self, job_id):
        for job in self.jobs:
            if job["id"] == job_id:
                return job

        return None

    def list_jobs(self, status=None, page=1, page_size=10):
        jobs = self.jobs

        if status:
            jobs = [job for job in jobs if job["status"] == status.upper()]

        start = (page - 1) * page_size
        return jobs[start : start + page_size]

    def close_job(self, job_id):
        job = self.get_job(job_id)

        if not job:
            return None

        if job["status"] == "CLOSED":
            raise ValueError("Job is already closed")

        job["status"] = "CLOSED"

        return job

    def add_application(self, job_id, candidate_name, candidate_email):
        job = self.get_job(job_id)

        if not job:
            return None

        if job["status"] == "CLOSED":
            raise ValueError("Job is closed and no longer accepting applications")

        for app in self.applications:
            if (
                app["job_id"] == job_id
                and app["candidate_email"].lower() == candidate_email.lower()
            ):
                raise ValueError("Candidate has already applied for this job")

        application = {
            "id": self._next_application_id,
            "job_id": job_id,
            "candidate_name": candidate_name,
            "candidate_email": candidate_email,
            "submitted_at": datetime.now(timezone.utc),
        }

        self._next_application_id += 1
        self.applications.append(application)

        return application

    def list_applications(self, job_id=None, candidate_name=None, page=1, page_size=10):
        applications = self.applications

        if job_id:
            applications = [
                app for app in applications if app["job_id"] == job_id
            ]

        if candidate_name:
            applications = [
                app
                for app in applications
                if app["candidate_name"].lower() == candidate_name.lower()
            ]

        start = (page - 1) * page_size
        return applications[start : start + page_size]