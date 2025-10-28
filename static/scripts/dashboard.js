document.addEventListener("DOMContentLoaded", function () {
    const uploadBtn = document.getElementById("upload-excel-btn");
    const refreshBtn = document.getElementById("refresh");
    const ctx = document.getElementById("studentsChart").getContext("2d");

        

    function getCSRFToken() {
        const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
        if (tokenInput) return tokenInput.value;

        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            if (cookie.trim().startsWith('csrftoken=')) {
                return cookie.trim().substring('csrftoken='.length);
            }
        }
        return '';
    }

    if (uploadBtn) {
        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.accept = ".xlsx";
        fileInput.style.display = "none";
        document.body.appendChild(fileInput);

        uploadBtn.addEventListener("click", function (e) {
            e.preventDefault();
            fileInput.click();
        });

        fileInput.addEventListener("change", function () {
            const file = fileInput.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append("file", file);

            fetch("/upload/export_xlsx/", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                },
            })
            .then(async (res) => {
                const text = await res.text();
                try {
                    const data = JSON.parse(text);
                    if (data.message) {
                        alert(data.message);
                        location.reload();
                    } else if (data.error) {
                        alert("Xatolik: " + data.error);
                    }
                } catch (err) {
                    console.error("HTML yoki JSON bo‘lmagan javob:", text);
                    alert("Serverdan noto‘g‘ri javob keldi. URL yoki view nomi tekshirilishi kerak.");
                }
            })
            .catch((err) => {
                console.error(err);
                alert("Xatolik yuz berdi: " + err.message);
            });
        });
    }

    if (refreshBtn) {
        refreshBtn.addEventListener("click", function (e) {
            e.preventDefault();
            if (!confirm("Barcha o‘quvchilarning statusini 'Bor' va sababini bo‘sh qilasizmi?")) return;

            fetch("/upload/set_null_all/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                },
            })
            .then(async (res) => {
                const text = await res.text();
                try {
                    const data = JSON.parse(text);
                    if (data.message) {
                        alert(data.message);
                        location.reload();
                    } else if (data.error) {
                        alert("Xatolik: " + data.error);
                    }
                } catch (err) {
                    console.error("HTML yoki JSON bo‘lmagan javob:", text);
                    alert("Serverdan noto‘g‘ri javob keldi.");
                }
            })
            .catch((err) => {
                console.error(err);
                alert("Xatolik yuz berdi: " + err.message);
            });
        });
    }
    function fetchDashboardData() {
        fetch("/dashboard_inf/")
            .then((response) => response.json())
            .then((data) => {
                const visited = data.visited;
                const total = data.total;
                const reason = data.reason;
                const no_reason = data.no_reason;

                new Chart(ctx, {
                    type: "doughnut",
                    data: {
                        labels: ["Kelganlar", "Kelmaganlar", "Sababli"],
                        datasets: [{
                            data: [visited, reason, no_reason],
                            backgroundColor: ["#00b624", "#f44336", "#ebcf00"],
                            borderWidth: 2,
                            hoverOffset: 10
                        }]
                    },
                    options: {
                        plugins: {
                            legend: { display: true, position: "bottom" },
                            tooltip: {
                                callbacks: {
                                    label: function (context) {
                                        let value = context.raw;
                                        let percent = total > 0 ? (value / total * 100).toFixed(1) : 0;
                                        return `${context.label}: ${value} (${percent}%)`;
                                    }
                                }
                            }
                        }
                    }
                });
            })
            .catch((err) => {
                console.error("Xatolik:", err);
                alert("Serverdan ma'lumot olishda xatolik yuz berdi.");
            });
    }

    fetchDashboardData();
});
