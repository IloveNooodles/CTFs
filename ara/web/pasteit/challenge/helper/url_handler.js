module.exports = {
    makeHyperLink(text) {
        // check if text contains a link
        if(text.includes("http") || text.includes("www.")) {
            // if it does, return the text with the link wrapped in an anchor tag
            return text.replace(/(http|www.)\S+/g, (match) => `<a class="text-blue-600 underline" href="${match}">${match}</a>`);
        }
        return text;
    }
}