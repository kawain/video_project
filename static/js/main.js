(function () {
    if (!document.getElementById("count")) {
        return
    }
    let count = Number(document.getElementById("count").textContent)
    const thumb = document.querySelectorAll(".thumb")
    const evaluation = document.querySelectorAll(".evaluation")
    const del = document.querySelectorAll(".del")
    const favorite = document.querySelectorAll(".favorite")
    const video = document.querySelector("#video")
    const uid = document.querySelector("#uid")
    const videoModal = document.getElementById("videoModal")
    const videoModalOBJ = new bootstrap.Modal(videoModal)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    for (const v of thumb) {
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
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            };
            fetch("/rank_update/", { method, headers, body })
                .then((res) => {
                    return res.json()
                })
                .then((json) => {
                    console.log(json)
                    if (json.ok === 1) {
                        e.target.classList.replace("btn-outline-primary", "btn-primary")
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
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            };
            fetch("/del_update/", { method, headers, body })
                .then((res) => {
                    return res.json()
                })
                .then((json) => {
                    if (json.ok === 1) {
                        e.target.parentNode.parentNode.parentNode.remove()
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

    // localStorage に追加
    for (const v of favorite) {
        v.addEventListener("click", (e) => {
            const name = e.target.dataset.name
            let favoriteArr
            if (localStorage.getItem("favorite") === null) {
                favoriteArr = []
            } else {
                //キーが favorite のものを取得してオブジェクトに変換
                favoriteArr = JSON.parse(localStorage.getItem("favorite"))
            }
            favoriteArr.push(name)
            localStorage.setItem("favorite", JSON.stringify(favoriteArr))
            e.target.classList.replace("btn-outline-info", "btn-info")
        })
    }

    lazyload()
}())

