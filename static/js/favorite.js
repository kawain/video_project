function delStorage(obj, name) {
    if (!window.confirm("本当に削除しますか？")) {
        return
    }
    const newArr = []
    arr = JSON.parse(localStorage.getItem("favorite"))
    for (const v of arr) {
        if (name === v) {

        } else {
            newArr.push(v)
        }
    }
    obj.parentNode.parentNode.remove()
    localStorage.setItem("favorite", JSON.stringify(newArr))
}

(function () {
    let playList = []
    let index = 0

    const favoriteList = document.getElementById("favoriteList")
    const video = document.querySelector(".videoTag video")
    const pre = document.getElementById("pre")
    const play = document.getElementById("play")
    const next = document.getElementById("next")
    const save = document.getElementById("save")
    const stop = document.getElementById("stop")
    const allDel = document.getElementById("allDel")

    function getStorage() {
        let arr
        if (localStorage.getItem("favorite") === null) {
            arr = []
        } else {
            arr = JSON.parse(localStorage.getItem("favorite"))
        }
        return arr
    }

    function playVideo(index) {
        const src = `/media/video/${playList[index]}.mp4`
        video.src = src
        video.load()
        video.play()
    }

    save.addEventListener("click", () => {
        const children = favoriteList.children
        const newArr = []
        playList = []
        for (const v of children) {
            newArr.push(v.dataset.name)
            playList.push(v.dataset.name)
        }
        localStorage.setItem("favorite", JSON.stringify(newArr))
    })

    video.addEventListener("ended", () => {
        index++
        if (playList.length === index) {
            index = 0
        }
        playVideo(index)
    })

    play.addEventListener("click", () => {
        playVideo(index)
    })

    pre.addEventListener("click", () => {
        index--
        if (0 > index) {
            index = playList.length - 1
        }
        playVideo(index)
    })

    next.addEventListener("click", () => {
        index++
        if (playList.length === index) {
            index = 0
        }
        playVideo(index)
    })

    stop.addEventListener("click", () => {
        index = 0
        video.src = ""
        video.load()
    })

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

    allDel.addEventListener("click", () => {
        if (!window.confirm("本当に削除しますか？")) {
            return
        }
        localStorage.clear()
        favoriteList.innerHTML = ""
        playList = []
        index = 0
        video.src = ""
        video.load()
    })

    const arr = getStorage()

    if (arr.length > 0) {
        let html = ""
        for (const v of arr) {
            html += `
<div class="favorite_box" data-name="${v}">
    <div class="favorite_box1">
        <button class="btn btn-sm btn-outline-warning del" data-name="${v}" onclick="delStorage(this, '${v}')">削除</button>
    </div>
    <div class="favorite_box2">
        <img src="/media/thumbnail/${v}.jpg">
    </div>
</div>`
        }

        favoriteList.innerHTML = html
    }

    new Sortable(favoriteList, {
        animation: 150,
    })

    window.addEventListener("DOMContentLoaded", () => {
        const children = favoriteList.children
        for (const v of children) {
            playList.push(v.dataset.name)
        }
    })

})()