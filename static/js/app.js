const available_queries = [
    'machine learning',
    'students affairs',
    'software',
    'graduate courses',
    'informatics',
    'REST',
    'computer games',
    'information',
    'PhD program',
    'artificial intelligence',
    'computer science'
]

const wordButtonsEl = document.querySelector('.word-btns');

available_queries.forEach((word) => {
    const wordBtnEl = document.createElement('button');
    wordBtnEl.className = 'ui button word-btn';
    wordBtnEl.appendChild(document.createTextNode(word))

    wordButtonsEl.appendChild(wordBtnEl);
})

wordButtonsEl.addEventListener('click', (e) => {
    if (e.target.className === 'ui button word-btn') {
        const searchBarEl = document.querySelector('#search-bar');
        searchBarEl.value = e.target.textContent
        searchBarEl.disabled = "disabled"
        searchBarEl.classList.add('disabled')
    }
})

document.querySelector('#search-form').addEventListener('submit', (e) =>{
    e.preventDefault();
    const wordBankBoxEl = document.querySelector('#word-bank-box');
    wordBankBoxEl.style.display = 'none';
    const searchLoadingEl = document.querySelector('#search-loading');
    searchLoadingEl.style.display = 'block';

    const searchBarEl = document.querySelector('#search-bar');
    searchBarEl.disabled = false;
    searchBarEl.classList.remove('disabled');


    setTimeout(async () => {
        const response = await fetch(`/api/search?query=${encodeURIComponent(searchBarEl.value)}`)
        if (response.status === 200) {
            const data = await response.json();
            console.log(data);
        }
        searchLoadingEl.style.display = 'none';
    }, 700)
})