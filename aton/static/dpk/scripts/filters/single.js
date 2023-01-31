import {templateItemSingle} from '../templates/filter.js'


// фильтр по компаниям
class FilterSingle {
    constructor(container, requests, path, key) {
        this.container = container;
        this.path = path;
        this.requests = requests;
        this.key = key;

        // контейнер с выбранными элементами и строкой поиска
        this.elemField = this.container.querySelector('.filter-field');
        this.elemFieldSpanInput = this.elemField.querySelector('span');
        this.elemInputValue = this.container.querySelector('.filter-input');
        this.elemClearFilter = this.container.querySelector('.filter-clear i');

        // контейнер с списком выбираемых элементов
        this.elemWindow = this.container.querySelector('.filter-window');
        this.elemWindowClose = this.elemWindow.querySelector('.filter-window-close');
        this.elemWindowContent = this.elemWindow.querySelector('.filter-window-content-one-col');
        this.spinnerLoad = this.elemWindow.querySelector('.spinner-load');
    }

    init() {
        this.initHandler();
    }
    
    initHandler() {
        // событие - установка курсора на поле
        this.elemInputValue.addEventListener('click', async (e) => {
            this.getAndRenderData();
        });
        // событие - ввод значения поля
        this.elemInputValue.addEventListener('input', async (e) => {
            let searchValue = e.target.value;
            this.getAndRenderData(searchValue);
        });
        // событие - клик по кнопке очистки фильтра
        this.elemClearFilter.addEventListener('click', (e) => {
            this.clearFilter();
        })
        // событие - клик по злементу списка
        this.elemWindowContent.addEventListener('click', (e) => {
            if (e.target.tagName === "LI") {
                console.log(e.target.dataset.name);
                this.insertValueInFilter(e.target.dataset.name);
            }
        })
        // событие - клик по кнопке закрытия окна выбора элементов 
        this.elemWindowClose.addEventListener('click', async (e) => {
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
        this.resizeWindow();
        this.elemWindow.classList.remove("d-none");
        this.elemWindowContent.innerHTML = "";
        this.spinnerLoad.classList.remove('d-none');
        let data = await this.getData(searchValue);
        // для отсутствия мелькания элемента загрузки
        setTimeout(() => {
            this.spinnerLoad.classList.add('d-none');
            this.renderData(data);
        }, 300)
    }

    // получение списка данных
    async getData(searchValue="") {
        const response = await this.requests.GET_LONG(this.path, {"search": searchValue});
        if (!response.error) {
            return response.result
        }
    }

    // вывод списка данных
    renderData(dataList) {
        let contentHTML = "";
        for (let obj of dataList) {
            contentHTML += templateItemSingle(obj[this.key]);
        }
        this.elemWindowContent.innerHTML = `
            <ul>
                ${contentHTML}
            </ul>
        `;
    }

    // очистка фильтра
    clearFilter() {
        this.elemInputValue.value = "";
    }

    // вставка значения в фильтр
    insertValueInFilter(value) {
        this.elemInputValue.value = value;
    }

    resizeWindow() {
        let size = this.elemField.getBoundingClientRect();
        let top = size.bottom;
        let left = size.left;
        let width = size.width;
        this.elemWindow.style.top = top + 12 + "px";
        this.elemWindow.style.left = left + "px";
        this.elemWindow.style.width = width + "px";
    }

    getRequestParameters() {
        return this.elemInputValue.value;
    }
}

export {FilterSingle, };

