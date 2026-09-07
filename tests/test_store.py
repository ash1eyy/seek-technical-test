import pytest

from store import Store


class TestAddJob:
    def test_returns_correct_fields(self):
        store = Store()
        job = store.add_job(title="Dev", description="Backend work", location="Melbourne")

        assert job["title"] == "Dev"
        assert job["description"] == "Backend work"
        assert job["location"] == "Melbourne"
        assert job["status"] == "OPEN"
        assert "id" in job
        assert "created_at" in job

    def test_ids_auto_increment(self):
        store = Store()
        job1 = store.add_job(title="A", description="", location="")
        job2 = store.add_job(title="B", description="", location="")

        assert job2["id"] == job1["id"] + 1


class TestGetJob:
    def test_found(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        result = store.get_job(job["id"])

        assert result == job

    def test_not_found(self):
        store = Store()
        assert store.get_job(999) is None


class TestListJobs:
    def test_all(self):
        store = Store()
        store.add_job(title="A", description="", location="")
        store.add_job(title="B", description="", location="")

        assert len(store.list_jobs()) == 2

    def test_filter_by_status(self):
        store = Store()
        j1 = store.add_job(title="A", description="", location="")
        store.add_job(title="B", description="", location="")
        store.close_job(j1["id"])

        open_jobs = store.list_jobs(status="OPEN")
        closed_jobs = store.list_jobs(status="CLOSED")

        assert len(open_jobs) == 1
        assert len(closed_jobs) == 1

    def test_pagination(self):
        store = Store()
        for i in range(5):
            store.add_job(title=f"Job {i}", description="", location="")

        page1 = store.list_jobs(page=1, page_size=2)
        page2 = store.list_jobs(page=2, page_size=2)
        page3 = store.list_jobs(page=3, page_size=2)

        assert len(page1) == 2
        assert len(page2) == 2
        assert len(page3) == 1


class TestCloseJob:
    def test_closes_open_job(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        result = store.close_job(job["id"])

        assert result["status"] == "CLOSED"

    def test_already_closed(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        store.close_job(job["id"])

        with pytest.raises(ValueError, match="already closed"):
            store.close_job(job["id"])

    def test_nonexistent(self):
        store = Store()
        assert store.close_job(999) is None


class TestOpenJob:
    def test_opens_closed_job(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        store.close_job(job["id"])
        result = store.open_job(job["id"])

        assert result["status"] == "OPEN"

    def test_already_open(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")

        with pytest.raises(ValueError, match="already open"):
            store.open_job(job["id"])

    def test_nonexistent(self):
        store = Store()
        assert store.open_job(999) is None


class TestAddApplication:
    def test_returns_correct_fields(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        app = store.add_application(
            job_id=job["id"],
            candidate_name="Alice",
            candidate_email="alice@example.com",
        )

        assert app["job_id"] == job["id"]
        assert app["candidate_name"] == "Alice"
        assert app["candidate_email"] == "alice@example.com"
        assert "id" in app
        assert "submitted_at" in app

    def test_ids_auto_increment(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        a1 = store.add_application(
            job_id=job["id"], candidate_name="A", candidate_email="a@test.com"
        )
        a2 = store.add_application(
            job_id=job["id"], candidate_name="B", candidate_email="b@test.com"
        )

        assert a2["id"] == a1["id"] + 1

    def test_closed_job(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        store.close_job(job["id"])

        with pytest.raises(ValueError, match="closed"):
            store.add_application(
                job_id=job["id"],
                candidate_name="A",
                candidate_email="a@test.com",
            )

    def test_duplicate_application(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        store.add_application(
            job_id=job["id"],
            candidate_name="Alice",
            candidate_email="alice@test.com",
        )

        with pytest.raises(ValueError, match="already applied"):
            store.add_application(
                job_id=job["id"],
                candidate_name="Alice",
                candidate_email="alice@test.com",
            )

    def test_duplicate_case_insensitive(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        store.add_application(
            job_id=job["id"],
            candidate_name="Alice",
            candidate_email="Alice@Test.com",
        )

        with pytest.raises(ValueError, match="already applied"):
            store.add_application(
                job_id=job["id"],
                candidate_name="Alice",
                candidate_email="alice@test.com",
            )

    def test_nonexistent_job(self):
        store = Store()
        assert store.add_application(
            job_id=999, candidate_name="A", candidate_email="a@test.com"
        ) is None


class TestListApplications:
    def test_all(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        store.add_application(
            job_id=job["id"], candidate_name="A", candidate_email="a@test.com"
        )
        store.add_application(
            job_id=job["id"], candidate_name="B", candidate_email="b@test.com"
        )

        assert len(store.list_applications()) == 2

    def test_filter_by_job_id(self):
        store = Store()
        j1 = store.add_job(title="A", description="", location="")
        j2 = store.add_job(title="B", description="", location="")
        store.add_application(
            job_id=j1["id"], candidate_name="X", candidate_email="x@test.com"
        )
        store.add_application(
            job_id=j2["id"], candidate_name="Y", candidate_email="y@test.com"
        )

        results = store.list_applications(job_id=j1["id"])
        assert len(results) == 1
        assert results[0]["job_id"] == j1["id"]

    def test_filter_by_candidate_name(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        store.add_application(
            job_id=job["id"], candidate_name="Alice Smith", candidate_email="a@test.com"
        )
        store.add_application(
            job_id=job["id"], candidate_name="Bob Jones", candidate_email="b@test.com"
        )

        results = store.list_applications(candidate_name="alice")
        assert len(results) == 1
        assert results[0]["candidate_name"] == "Alice Smith"

    def test_candidate_name_partial_match(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        store.add_application(
            job_id=job["id"],
            candidate_name="Alice Smith",
            candidate_email="a@test.com",
        )

        results = store.list_applications(candidate_name="Smith")
        assert len(results) == 1

    def test_pagination(self):
        store = Store()
        job = store.add_job(title="X", description="", location="")
        for i in range(5):
            store.add_application(
                job_id=job["id"],
                candidate_name=f"Candidate {i}",
                candidate_email=f"c{i}@test.com",
            )

        page1 = store.list_applications(page=1, page_size=2)
        page2 = store.list_applications(page=2, page_size=2)
        page3 = store.list_applications(page=3, page_size=2)

        assert len(page1) == 2
        assert len(page2) == 2
        assert len(page3) == 1
