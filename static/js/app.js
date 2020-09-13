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
const wordBankBoxEl = document.querySelector('#word-bank-box');
const resultBox = document.querySelector('#result-box');
const resultTBodyEl = document.querySelector('#search-result');

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

document.querySelector('#search-form').addEventListener('submit', (e) => {
    e.preventDefault();
    resultBox.style.display = 'none';
    resultTBodyEl.innerHTML = '';
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

            if (data.length === 0) {
                return;
            }

            data.forEach((result) => {
                const rowEl = document.createElement('tr');
                rowEl.innerHTML = `
                    <td class="center aligned collapsing rank">${result[0]}</td>
                    <td class="url">
                        <a class="item" target="_blank" href="${result[1].startsWith('http') ? result[1] : 'http://' + result[1]}">${result[1]}</a>
                    </td>
                `;
                resultTBodyEl.appendChild(rowEl)

            })
        }
        searchLoadingEl.style.display = 'none';
        resultBox.style.display = 'block';
    }, 500)
})


document.querySelector('#search-bar').addEventListener('click', () => {
    wordBankBoxEl.style.display = 'block';
    resultBox.style.display = 'none';
})

document.querySelector('#back-to-word-bank-btn').addEventListener('click', () => {
    wordBankBoxEl.style.display = 'block';
    resultBox.style.display = 'none';
})

document.querySelector('#about-link').addEventListener('click', (e) => {
    e.preventDefault();
    $('.ui.basic.modal')
        .modal('show')
    ;
})