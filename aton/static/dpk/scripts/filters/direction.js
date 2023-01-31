import {templateCartCompanyElement, templateCartDirectionElement, templateSelectItemElement, } from '../templates/filter.js'


// фильтр по компаниям
export default class FilterDirection {
    constructor(container, requests, path) {
        this.container = container;
        this.path = path;
        this.requests = requests;

        // контейнер с выбранными элементами и строкой поиска
        this.elemFilterField = this.container.querySelector('.filter-field');
        this.elemFilterSpanInput = this.elemFilterField.querySelector('span');
        // строка поиска элемента
        this.elemFilterInput = this.container.querySelector('.filter-input');
        this.elemFilterClear = this.container.querySelector('.filter-clear i');
        
        // контейнер с карточками выбираемых элементов
        this.elemWindow = this.container.querySelector('.filter-window-data');
        this.elemWindowContent = this.container.querySelector('.filter-window-data-content');
        this.elemBtnCloseWindow = this.container.querySelector('.filter-window-data-close button');
        this.spinnerLoad = this.container.querySelector('.spinner-load');
        
    }

    async init() {
        await this.getAndRenderData();
        this.initHandlerField();
        this.initHandlerWindow();
    }

    initHandlerField() {
        // событие - установка курсора на поле
        this.elemFilterInput.addEventListener('click', async (e) => {
            this.resizeWindow();
            this.showWindow();
        });
        // событие - клик по кнопке удаления выбранного элемента
        this.elemFilterField.addEventListener('click', (e) => {
            const itemElem = e.target.closest(".filter-item");
            const btnDelElem = e.target.closest(".filter-item-delete");
            if (itemElem && btnDelElem) {
                e.stopPropagation();
                let id_bx = itemElem.dataset.idBx;
                itemElem.remove();
                this.uncheckElementForWindow(id_bx);
            }
        })
        // событие - клик по кнопке очистки фильтра
        this.elemFilterClear.addEventListener('click', (e) => {
            this.clearFilter();
        })
        // событие - изменение размера поля
        $(this.elemFilterField).bind("DOMSubtreeModified", (e) => {
            this.resizeWindow();
        })
    }

    initHandlerWindow() {
        // событие - клик по полю ввода
        this.elemWindowContent.addEventListener('input', (e) => {
            if (e.target.checked) {
                this.addElementToFilter(e.target.dataset.idBx, e.target.value);
            } else {
                this.removeElementFromFilter(e.target.dataset.idBx);
            }
        })

        // событие - клик по кнопке закрытия окна выбора элементов 
        this.elemBtnCloseWindow.addEventListener('click', async (e) => {
            this.elemWindow.classList.add("d-none");
        })
        // событие - клик вне окна выбора элементов 
        document.addEventListener('click', async (e) => {
            if (e.target.closest(".filter") !== this.container) {
                this.elemWindow.classList.add("d-none");
            }
        })
    }

    async getAndRenderData(searchValue="") {
        
        let data = await this.getData(searchValue);
        this.renderData(data);
    }

    // получение списка данных
    async getData(searchValue="") {
        const response = await this.requests.GET_LONG(this.path, {"search": searchValue});
        if (!response.error) {
            return response.result
        }
    }

    renderData(dataList) {
        let contentHTML = "";
        for (let obj of dataList) {
            contentHTML += templateCartDirectionElement(obj.id_bx, obj.name);
        }
        this.elemWindowContent.innerHTML = `
            <ul>
                ${contentHTML}
            </ul>
        `;
    }

    showWindow() {
        this.elemWindow.classList.remove("d-none");
    }

    // добавить элемент в поле фильтра
    addElementToFilter(id_bx, name) {
        const insertElem = templateSelectItemElement(id_bx, name);
        this.elemFilterSpanInput.insertAdjacentHTML('beforebegin', insertElem);
    }

    // удаление элемента из фильтра
    removeElementFromFilter(id_bx) {
        let itemList = this.elemFilterField.querySelectorAll(".filter-item");
        for (let item of itemList) {
            if (item.dataset.idBx == id_bx) {
                item.remove();
            }
        }
    }

    // очистка фильтра
    clearFilter() {
        const selectedItems = this.elemFilterField.getElementsByClassName("filter-item");
        const items = this.elemWindow.querySelectorAll("input");
        while(selectedItems.length > 0) {
            selectedItems[0].remove();
        }
        items.forEach((input) => input.checked = false)
    }
 
    // удаление элемента из фильтра
    uncheckElementForWindow(id_bx) {
        const items = this.elemWindow.querySelectorAll("input");
        for (let item of items) {
            if (item.dataset.idBx == id_bx) {
                item.checked = false;
            }
        }
    }
    // получить параметры филитрации для выполнения запроса
    getRequestParameters() {
        const selectedItems = this.elemFilterField.getElementsByClassName("filter-item");
        let idCompanies = [];
        for (let item of selectedItems) {
            idCompanies.push(item.dataset.idBx);
        }
        return idCompanies;
    }

    resizeWindow() {
        let size = this.elemFilterField.getBoundingClientRect();
        let top = size.bottom;
        let left = size.left;
        let width = size.width;
        this.elemWindow.style.top = top + 12 + "px";
        this.elemWindow.style.left = left + "px";
        this.elemWindow.style.width = width + "px";
    }
}
