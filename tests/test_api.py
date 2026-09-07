class TestJobsEndpoint:
    def test_list_jobs_empty(self, client):
        response = client.get("/jobs")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_job(self, client):
        response = client.post(
            "/jobs/create",
            json={
                "title": "Backend Engineer",
                "description": "Build stuff",
                "location": "Melbourne",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Backend Engineer"
        assert data["status"] == "OPEN"
        assert "id" in data

    def test_list_jobs_after_create(self, client):
        client.post(
            "/jobs/create",
            json={"title": "A", "description": "", "location": ""},
        )
        response = client.get("/jobs")
        assert len(response.json()) == 1

    def test_get_job(self, client):
        create = client.post(
            "/jobs/create",
            json={"title": "X", "description": "", "location": ""},
        )
        job_id = create.json()["id"]
        response = client.get(f"/jobs/{job_id}")
        assert response.status_code == 200
        assert response.json()["id"] == job_id

    def test_get_job_404(self, client):
        response = client.get("/jobs/999")
        assert response.status_code == 404

    def test_close_job(self, client):
        create = client.post(
            "/jobs/create",
            json={"title": "X", "description": "", "location": ""},
        )
        job_id = create.json()["id"]
        response = client.post(f"/jobs/{job_id}/close")
        assert response.status_code == 200
        assert response.json()["status"] == "CLOSED"

    def test_close_already_closed(self, client):
        create = client.post(
            "/jobs/create",
            json={"title": "X", "description": "", "location": ""},
        )
        job_id = create.json()["id"]
        client.post(f"/jobs/{job_id}/close")
        response = client.post(f"/jobs/{job_id}/close")
        assert response.status_code == 400

    def test_close_nonexistent(self, client):
        response = client.post("/jobs/999/close")
        assert response.status_code == 404

    def test_open_job(self, client):
        create = client.post(
            "/jobs/create",
            json={"title": "X", "description": "", "location": ""},
        )
        job_id = create.json()["id"]
        client.post(f"/jobs/{job_id}/close")
        response = client.post(f"/jobs/{job_id}/open")
        assert response.status_code == 200
        assert response.json()["status"] == "OPEN"

    def test_open_already_open(self, client):
        create = client.post(
            "/jobs/create",
            json={"title": "X", "description": "", "location": ""},
        )
        job_id = create.json()["id"]
        response = client.post(f"/jobs/{job_id}/open")
        assert response.status_code == 400

    def test_list_jobs_filter_status(self, client):
        client.post(
            "/jobs/create",
            json={"title": "A", "description": "", "location": ""},
        )
        create2 = client.post(
            "/jobs/create",
            json={"title": "B", "description": "", "location": ""},
        )
        client.post(f"/jobs/{create2.json()['id']}/close")

        open_jobs = client.get("/jobs?status=OPEN").json()
        closed_jobs = client.get("/jobs?status=CLOSED").json()
        assert len(open_jobs) == 1
        assert len(closed_jobs) == 1


class TestApplicationsEndpoint:
    def test_list_applications_empty(self, client):
        response = client.get("/applications")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_application(self, client):
        create = client.post(
            "/jobs/create",
            json={"title": "X", "description": "", "location": ""},
        )
        job_id = create.json()["id"]
        response = client.post(
            "/applications/create",
            json={
                "job_id": job_id,
                "candidate_name": "Alice",
                "candidate_email": "alice@example.com",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["candidate_name"] == "Alice"
        assert data["job_id"] == job_id

    def test_create_application_closed_job(self, client):
        create = client.post(
            "/jobs/create",
            json={"title": "X", "description": "", "location": ""},
        )
        job_id = create.json()["id"]
        client.post(f"/jobs/{job_id}/close")
        response = client.post(
            "/applications/create",
            json={
                "job_id": job_id,
                "candidate_name": "Alice",
                "candidate_email": "alice@example.com",
            },
        )
        assert response.status_code == 400

    def test_create_application_nonexistent_job(self, client):
        response = client.post(
            "/applications/create",
            json={
                "job_id": 999,
                "candidate_name": "Alice",
                "candidate_email": "alice@example.com",
            },
        )
        assert response.status_code == 404

    def test_create_application_duplicate(self, client):
        create = client.post(
            "/jobs/create",
            json={"title": "X", "description": "", "location": ""},
        )
        job_id = create.json()["id"]
        payload = {
            "job_id": job_id,
            "candidate_name": "Alice",
            "candidate_email": "alice@example.com",
        }
        client.post("/applications/create", json=payload)
        response = client.post("/applications/create", json=payload)
        assert response.status_code == 400

    def test_list_applications_after_create(self, client):
        create = client.post(
            "/jobs/create",
            json={"title": "X", "description": "", "location": ""},
        )
        job_id = create.json()["id"]
        client.post(
            "/applications/create",
            json={
                "job_id": job_id,
                "candidate_name": "Alice",
                "candidate_email": "alice@example.com",
            },
        )
        response = client.get("/applications")
        assert len(response.json()) == 1

    def test_list_applications_filter_job_id(self, client):
        j1 = client.post(
            "/jobs/create",
            json={"title": "A", "description": "", "location": ""},
        )
        j2 = client.post(
            "/jobs/create",
            json={"title": "B", "description": "", "location": ""},
        )
        client.post(
            "/applications/create",
            json={
                "job_id": j1.json()["id"],
                "candidate_name": "Alice",
                "candidate_email": "alice@example.com",
            },
        )
        client.post(
            "/applications/create",
            json={
                "job_id": j2.json()["id"],
                "candidate_name": "Bob",
                "candidate_email": "bob@example.com",
            },
        )
        response = client.get(f"/applications?job_id={j1.json()['id']}")
        assert len(response.json()) == 1
        assert response.json()[0]["job_id"] == j1.json()["id"]

    def test_list_applications_filter_candidate(self, client):
        create = client.post(
            "/jobs/create",
            json={"title": "X", "description": "", "location": ""},
        )
        job_id = create.json()["id"]
        client.post(
            "/applications/create",
            json={
                "job_id": job_id,
                "candidate_name": "Alice Smith",
                "candidate_email": "alice@example.com",
            },
        )
        client.post(
            "/applications/create",
            json={
                "job_id": job_id,
                "candidate_name": "Bob Jones",
                "candidate_email": "bob@example.com",
            },
        )
        response = client.get("/applications?candidate_name=alice")
        assert len(response.json()) == 1
        assert response.json()[0]["candidate_name"] == "Alice Smith"
