function addPaste() {
    const paste = document.getElementById("paste").value;
    console.log("test")
    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            paste: paste
        })
    })
    .then((response) => response.json())
    .then((data) => {
        return window.location.href = `/${data.id}`;
    });
}

const submit = document.getElementById("submit");
if(submit) {
    submit.addEventListener("click", addPaste);
}