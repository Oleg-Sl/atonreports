import {templateCartCompanyElement, templateCartDirectionElement, templateSelectItemElement, } from '../templates/filter.js'


// фильтр по компаниям
class FilterMultiple {
    constructor(container, requests, path) {
        this.container = container;
        this.path = path;
        this.requests = requests;
        // this.keyParamReq = keyParamReq;

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

    init() {
        this.initHandler();
    }

    initHandler() {
        // событие - установка курсора на поле
        this.elemFilterInput.addEventListener('click', async (e) => {
            this.getAndRenderData();
        });

        // событие - ввод значения поля
        this.elemFilterInput.addEventListener('input', async (e) => {
            let searchValue = e.target.value;
            this.getAndRenderData(searchValue);
        });
        
        // событие - клик по кнопке удаления выбранного элемента
        this.elemFilterField.addEventListener('click', (e) => {
            const itemElem = e.target.closest(".filter-item");
            const btnDelElem = e.target.closest(".filter-item-delete");
            if (itemElem && btnDelElem) {
                e.stopPropagation();
                itemElem.remove();
            }
        })

        this.elemFilterClear.addEventListener('click', (e) => {
            this.clearFilter();
        })

        $(this.elemFilterField).bind("DOMSubtreeModified", (e) => {
            this.resizeWindow();
        })

        // событие - клик по карточке в окне выбора злемента
        this.elemWindowContent.addEventListener('click', (e) => {
            const cartElem = e.target.closest(".filter-window-cart");
            if (cartElem) {
                this.addElementToFilter(
                    cartElem.dataset.idBx,
                    cartElem.dataset.name
                );
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

    // проверка выбран элемент или нет
    elementAlreadySelected(id_bx) {
        const selectedItems = this.elemFilterField.querySelectorAll(".filter-item");
        for (let item of selectedItems) {
            if (id_bx == item.dataset.idBx) return;
        }
        return true;
    }

    // добавить элемент в поле фильтра
    addElementToFilter(id_bx, name) {
        if (this.elementAlreadySelected(id_bx)) {
            const insertElem = templateSelectItemElement(id_bx, name);
            this.elemFilterSpanInput.insertAdjacentHTML('beforebegin', insertElem);
        }
        
    }

    // очистка фильтра
    clearFilter() {
        const selectedItems = this.elemFilterField.getElementsByClassName("filter-item");
        while(selectedItems.length > 0) {
            selectedItems[0].remove();
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
        // {
        //     keyParamReq: idCompanies.join(",")
        // };
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
