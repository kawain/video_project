let count = Number(document.getElementById("count").textContent)
const imgs = document.querySelectorAll("img")
const evaluation = document.querySelectorAll(".evaluation")
const del = document.querySelectorAll(".del")
const video = document.querySelector("#video")
const uid = document.querySelector("#uid")
const videoModal = document.getElementById("videoModal")
const videoModalOBJ = new bootstrap.Modal(videoModal)

for (const v of imgs) {
    v.addEventListener("click", (e) => {
        const filename = e.target.dataset.name
        uid.innerHTML = filename
        videoModalOBJ.toggle()
        video.src = `/media/video/${filename}.mp4`
        video.load()
        video.play()
    })
}

videoModal.addEventListener("hidden.bs.modal", () => {
    video.src = ""
    uid.innerHTML = ""
    video.load()
})

for (const v of evaluation) {
    v.addEventListener("click", (e) => {
        const id = e.target.dataset.name
        const val = document.getElementById(`select_${id}`).value
        const obj = {
            name: id,
            select: val
        }
        const method = "POST";
        const body = JSON.stringify(obj);
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        };
        fetch("/rank_update", { method, headers, body })
            .then((res) => {
                return res.json()
            })
            .then((json) => {
                if (json.ok === 1) {
                    e.target.classList.replace("btn-outline-secondary", "btn-secondary")
                }
            })
            .catch((e) => {
                console.log("エラー ", e)
            });
    })
}

for (const v of del) {
    v.addEventListener("click", (e) => {
        if (!window.confirm("本当に削除しますか？")) {
            return
        }
        const id = e.target.dataset.name
        const obj = { name: id }
        const method = "POST";
        const body = JSON.stringify(obj);
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        };
        fetch("/del_update", { method, headers, body })
            .then((res) => {
                return res.json()
            })
            .then((json) => {
                if (json.ok === 1) {
                    e.target.parentNode.parentNode.remove()
                    count--
                    document.getElementById("count").innerHTML = count

                }
            })
            .catch((e) => {
                console.log("エラー ", e)
            });
    })
}

video.addEventListener("keydown", (e) => {
    switch (e.keyCode) {
        case 65:
            e.preventDefault();
            video.currentTime -= 10;
            break;

        case 68:
            e.preventDefault();
            video.currentTime += 30;
            break;

    }
})

lazyload();