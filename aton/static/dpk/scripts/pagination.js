export default class Paginator {
    constructor(paginatorElement) {
        this.paginatorElement = paginatorElement;                                           // контейнер пагинатора
        // this.app = app;
        this.containerUl = this.paginatorElement.querySelector("ul");       // контейнер с элементами пагинатора
        this.init();
    }

    init() {
        
    }

    // получить элемент пагинатора
    getElementsHTML(page, currentPage="") {
        let active = page == currentPage ? "active" : "";                   // выделение номера текущей страницы
        let disabled = page == "..." ? "disabled" : "";                     // отключение активности элемента пагинатора
        return `<li class="page-item ${active} ${disabled}"><a class="page-link" data-page="${page}">${page}</a></li>`;
    }

    // рендер пагинатора с учетом текущей страницы
    render(page, countPage) {
        this.containerUl.innerHTML = "";                                                    // очистка пагинатора
        let leftRef  = page == 1 ? "disabled" : "";                                         // если текущая страница первая, то левая ссылка инактивна
        let rightRef = page == countPage ? "disabled" : "";                                 // если текущая страница последняя, то правая ссылка инактивна
        let contenpPaginator = `
            <li class="page-item ${leftRef}">
                <a class="page-link" aria-label="Previous" data-page="${page - 1}">
                    <span aria-hidden="true" data-page="${page - 1}">&laquo;</span>
                </a>
            </li>
        `;
        
        if (countPage < 10) {
            for (let i = 1; i <= countPage; i += 1) {
                contenpPaginator += this.getElementsHTML(i, page);
            }
        }
        else if(page < 6) {     
            let endNumber = 7;
            for (let i = 1; i <= endNumber; i++) {
                contenpPaginator += this.getElementsHTML(i, page);
            }
            contenpPaginator += this.getElementsHTML("...", page);
            contenpPaginator += this.getElementsHTML(countPage, page);
        }
        else if((countPage - page) < 5) {
            let startNumber = countPage - 6
            contenpPaginator += this.getElementsHTML(1, page);
            contenpPaginator += this.getElementsHTML("...", page);
            for (let i = startNumber; i <= countPage; i += 1) {
                contenpPaginator += this.getElementsHTML(i, page);
            }
    
        }
        else {
            contenpPaginator += this.getElementsHTML(1, page);
            contenpPaginator += this.getElementsHTML("...");
            for (let i = page - 2; i <= page + 2; i += 1) {
                contenpPaginator += this.getElementsHTML(i, page);
            }
            contenpPaginator += this.getElementsHTML("...");
            contenpPaginator += this.getElementsHTML(countPage, page);
        }

        contenpPaginator += `
            <li class="page-item ${rightRef}">
                <a class="page-link" aria-label="Next" data-page="${page + 1}">
                    <span aria-hidden="true" data-page="${page + 1}">&raquo;</span>
                </a>
            </li>
        `;
    
        this.containerUl.innerHTML = contenpPaginator; 
    }
}






class Paginatorrr {
    constructor(container) {
        this.container = container;
        this.currentPageNumber = 1;

    }

    initHandler() {
        this.container.addEventListener('click', async (e) => {
            if (e.target.tagNmae === "A") {
                let page = parseInt(e.target.dataset.page);
            }

        });
    }

    highlightPageNumber(page) {

    }

    // обработчик событий пагинатора
    initHandlerPaginator() {
        this.paginatorContent.onclick = (event) => {
            let page = event.target.dataset.page;
            if (page) {
                // устанавливаем требуемую страницу для получения данных
                this.page = +page;
                // получение данных статистики и вывод их в таблицу
                this.getData();
            }
        };
    }

    // получение элемента HTML пагинатора
    getElemPaginHTML(page) {
        // выделение номера текущей страницы
        let active = page == this.page ? "active" : "";
        // отключение активности элемента пагинатора
        let disabled = page == "..." ? "disabled" : "";
        return `<li class="page-item ${active} ${disabled}"><a class="page-link" href="#" data-page="${page}">${page}</a></li>`;
    }
    
    // рендер пагинатора с учетом текущей страницы
    paginator() {
        this.paginatorContent.innerHTML = "";
        this.paginatorContent.innerHTML = "";
        let leftRef = this.page == 1 ? "disabled" : "";
        let rightRef = this.page == this.countPage ? "disabled" : "";
        let contenpPaginator = `
            <li class="page-item ${leftRef}">
                <a class="page-link" href="#" aria-label="Previous" data-page="${this.page - 1}">
                    <span aria-hidden="true" data-page="${this.page - 1}">&laquo;</span>
                </a>
            </li>
        `;
        
        if (this.countPage < 6) {
            // если количество страниц меньше 6
            for (let i = 1; i <= this.countPage; i += 1) {
                contenpPaginator += this.getElemPaginHTML(i);
            }
        }
        else if(this.page < 5) {
            // если текущая страница меньше 5
            let endNumber = this.page == 1 ? 3 : +this.page + 1;
            for (let i = 1; i <= endNumber; i++) {
                contenpPaginator += this.getElemPaginHTML(i);
            }
            contenpPaginator += this.getElemPaginHTML("...");
            contenpPaginator += this.getElemPaginHTML(this.countPage);
        }
        else if((this.countPage - this.page) < 4) {
            // если текщая страница ольше 3 или меньше максимального количества страниц на 3
            let startNumber = (this.countPage - this.page) == 0 ? this.page - 2 : this.page - 1;
            contenpPaginator += this.getElemPaginHTML(1);
            contenpPaginator += this.getElemPaginHTML("...");
            for (let i =startNumber; i <= this.countPage; i += 1) {
                contenpPaginator += this.getElemPaginHTML(i);
            }
    
        }
        else {
            contenpPaginator += this.getElemPaginHTML(1);
            contenpPaginator += this.getElemPaginHTML("...");
            for (let i = this.page - 1; i <= this.page + 1; i += 1) {
                contenpPaginator += this.getElemPaginHTML(i);
            }
            contenpPaginator += this.getElemPaginHTML("...");
            contenpPaginator += this.getElemPaginHTML(this.countPage);
        }

        contenpPaginator += `
            <li class="page-item ${rightRef}">
                <a class="page-link" href="#" aria-label="Next" data-page="${this.page + 1}">
                <span aria-hidden="true" data-page="${this.page + 1}">&raquo;</span>
                </a>
            </li>
        `;
    
        this.paginatorContent.innerHTML = contenpPaginator; 
    }
}

