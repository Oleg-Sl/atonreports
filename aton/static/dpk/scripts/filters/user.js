import {templateSelectItemElement, templateUserBoxForSearch, templateDepartContainerBox, templateUserBoxForSelected, templateInputSearchUser} from '../templates/filter.js'


// Окно ПОИСК ПОЛЬЗОВАТЕЛЯ
export default class WindowSearchUser {
    constructor(container, bx) {
        this.container = container;
        this.bx = bx;

        // поле с выбранными сотрудниками и поиском
        this.field = this.container.querySelector(".filter-field");
        // поле поиска сотрудников
        this.fieldInput = this.field.querySelector("input");
        this.fieldSpanInput = this.field.querySelector("span");
        // кнопка очистки фильтра
        this.btnClearFilter = this.container.querySelector(".filter-clear");

        // окно выбора сотрудников (выводится список сотрудников и подразделений)
        this.window = this.container.querySelector(".window-user-search");
        
        

        this.timeAnimate = 1000/100;     // скорость анимации разворачивания/сворачивания списка подразделений - мс./пикс.
        // this.departContainer = this.container.querySelector(".container-data-depart");              // контейнер с подразделениями
        // this.departChoiceContainer = this.container.querySelector(".container-data-head-selector"); // контейнер с выбранными
        // this.departSearchInput = this.departChoiceContainer.querySelector("input");                 // контейнер ввода слова для поиска сотрудника
        
        this.boxResponsible = this.window.querySelector(".container-data-user");                    // окно ПОИСКА
        this.boxDepartment = this.window.querySelector(".container-data-depart");                   // окно ПОДРАЗДЕЛЕНИЙ

        this.btnResponsible = this.window.querySelector(".btn-search-responsible");                 // кнопка открыть "окно ПОИСК"
        this.btnDepartment = this.window.querySelector(".btn-search-department");                   // кнопка открыть "окно ОТДЕЛЫ"

        this.btnCloseWindow = this.window.querySelector(".filter-window-data-close button");        // кнопка закрыть окно


        
        this.departments = null;
    }

    async init() {
        // получение списка подразделений компаниии
        await this.getDepartments();
        // вывод списка подразделений
        this.renderDepartment();
        // инициализация обработчиков
        this.initHandler();
    }

    initHandler() {
        // событие "открытие окна поиска"
        this.btnResponsible.addEventListener("click", async (e) => {
            // this.fieldInput.classList.remove("d-none")
            this.fieldInput.removeAttribute("readonly");
            // this.departChoiceContainer.querySelector("input").classList.remove("d-none")
            this.btnResponsible.classList.remove("btn-search-inactive");
            this.btnDepartment.classList.add("btn-search-inactive");
            this.boxResponsible.classList.remove("d-none");
            this.boxDepartment.classList.add("d-none");

        })
        // событие "открытие окна подразделения"
        this.btnDepartment.addEventListener("click", async (e) => {
            // this.fieldInput.classList.add("d-none");
            this.fieldInput.setAttribute("readonly", true)
            // this.departChoiceContainer.querySelector("input").classList.add("d-none")
            this.btnResponsible.classList.add("btn-search-inactive");
            this.btnDepartment.classList.remove("btn-search-inactive");
            this.boxResponsible.classList.add("d-none");
            this.boxDepartment.classList.remove("d-none");
        })

        this.fieldInput.addEventListener("click", async (e) => {
            this.showWindow();
            let name = e.target.value;
            this.getAndDisplayUsersSearch(name);
        })
        // событие "поиск пользователя"
        this.fieldInput.addEventListener("input", async (e) => {
            this.showWindow();
            let name = e.target.value;
            this.getAndDisplayUsersSearch(name);
        })
        // событие "добавление пользователя в выбранные"
        this.container.addEventListener("click", async (e) => {
            let boxUser = e.target.closest(".ui-selector-user-box");            // блок-контейнер пользователя, по которому произошел клик
            // если клик не по кнопке "информация о сотруднике"
            if (boxUser && !e.target.closest(".ui-selector-item-user-link")) {
                let userId = boxUser.dataset.userId;
                let lastname = boxUser.dataset.lastname;
                let name = boxUser.dataset.name;
                let userType = boxUser.dataset.userType;

                this.addChoiceUser(userId, lastname, name, userType);
            }
        })
        // событие "клик разворачивание/сворачивание списка вложенных подразделений"
        this.boxDepartment.addEventListener("click", async (e) => {
            if (e.target.closest(".ui-selector-item-indicator")) {
                let box = e.target.closest(".ui-selector-item-box");            // блок-контейнер подразделения, по которому произошел клик
                let boxChildren = box.querySelector(".ui-selector-item-children");  // блок-контейнер с дочерними подразделениями родителя, по которому произошел клик
                let departId = box.dataset.departId;                                // id подразделения
                let usersDisplay = box.dataset.userDisplay;                         // список работников выведен/не выведен ("true"/"")
                if (!usersDisplay && departId) {
                    this.getAndDisplayUsersOfdepart(departId, boxChildren);         // получение и вывод списка работников подразделения
                    box.dataset.userDisplay = true;                                 // статус, что сотрудники подразделения уже выведены
                }
                if (box.classList.contains("ui-selector-item-box-open")) {
                    // свернуть вложенные подразделения
                    this.animationClose(boxChildren);
                    box.classList.remove("ui-selector-item-box-open");              // удаляем класс, что вложенные подразделения развернуты
                } else {
                    // развернуть вложенные подразделения
                    this.animationOpen(boxChildren);
                    box.classList.add("ui-selector-item-box-open");                 // добавляем класс, что вложенные подразделения развернуты
                }
            }
        })
        // событие "открытие страницы с информацией о сотруднике"
        this.container.addEventListener("click", async (e) => {
            if (e.target.classList.contains("ui-selector-item-user-link")) {
                let boxUser = e.target.closest(".ui-selector-user-box");            // блок-контейнер пользователя, по которому произошел клик
                let userId = boxUser.dataset.userId; 
                let path = `/company/personal/user/${userId}/`;
                console.log(path);
                await this.bx.openPath(path);
            }
            if (e.target.closest(".user-item-content") && !e.target.classList.contains("user-item-remove")) {
                let boxUser = e.target.closest(".user-item");                       // блок-контейнер пользователя, по которому произошел клик
                let userId = boxUser.dataset.userId; 
                let path = `/company/personal/user/${userId}/`;
                console.log(path);
                await this.bx.openPath(path); 
            }
            
        })
        // событие - очистить фильтр
        this.btnClearFilter.addEventListener('click', (e) => {
            this.clearFilter();
        })
        // событие "удалить пользователя из выбранных"
        this.field.addEventListener("click", async (e) => {
            const itemElem = e.target.closest(".filter-item");
            const btnDelElem = e.target.closest(".filter-item-delete");
            if (itemElem && btnDelElem) {
                e.stopPropagation();
                itemElem.remove();
            }
        })
        this.btnCloseWindow.addEventListener('click', (e) => {
            this.hideWindow();
        })
        // событие "скрыть окно выбора пользователей"
        document.addEventListener("click", async (e) => {
            if (e.target.closest(".filter") !== this.container) {
                this.hideWindow();
            }
        })
        // событие изменение значения фильтра
        $(this.field).bind("DOMSubtreeModified", (e) => {
            this.resizeWindow();
        })

    }

    showWindow() {
        this.resizeWindow();
        // this.userConyainer = userConyainer;
        this.window.classList.remove("d-none");
        // let left = x - this.container.offsetWidth;
        // let top = y + 50;
        // this.container.style.left = Math.max(0, left) + "px";
        // this.container.style.top = top + "px";
    }

    hideWindow() {
        this.window.classList.add("d-none");
    }

    // получение и вывод списка работников в окне поиска
    async getAndDisplayUsersSearch(name) {
        let contentHTML = "";
        let users = await this.bx.callMethod("user.search", {                             // получение списка пользователей подразделения из Битрикс
            "FILTER": {"NAME": `${name}%`, "ACTIVE": true}
        });
        let usersByLastname = await this.bx.callMethod("user.search", {                             // получение списка пользователей подразделения из Битрикс
            "FILTER": {"LAST_NAME": `${name}%`, "ACTIVE": true}
        });
        users.concat(usersByLastname);
        // let users = USERS;
        for (let user of users) {
            contentHTML += templateUserBoxForSearch(user.ID, user.LAST_NAME, user.NAME, user.WORK_POSITION, user.USER_TYPE);
        }
        this.boxResponsible.innerHTML = contentHTML;
    }

    // добавление пользователя в окно выбранных пользователей
    addChoiceUser(id, lastname, name, usertype) {
        if (this.addUserIsAllowedToFilter(id)) {
            let contentHTML = templateSelectItemElement(id, lastname + name);
            this.fieldSpanInput.insertAdjacentHTML('beforebegin', contentHTML);
        }
    }

    // проверка выбран элемент или нет
    addUserIsAllowedToFilter(id_bx) {
        const selectedItems = this.field.querySelectorAll(".filter-item");
        for (let item of selectedItems) {
            if (id_bx == item.dataset.idBx) return;
        }
        return true;
    }

    // очистка фильтра
    clearFilter() {
        const selectedItems = this.field.getElementsByClassName("filter-item");
        while(selectedItems.length > 0) {
            selectedItems[0].remove();
        }
    }
    
    resizeWindow() {
        let size = this.field.getBoundingClientRect();
        let top = size.bottom;
        let left = size.left;
        let width = size.width;
        this.window.style.top = top + 2 + "px";
        this.window.style.left = left + "px";
        this.window.style.width = width + "px";
    }


    // получение и вывод списка работников подразделения
    async getAndDisplayUsersOfdepart(departId, box) {
        let contentHTML = "";
        let users = await this.bx.callMethod("user.get", {                               // получение списка пользователей подразделения из Битрикс
            "ACTIVE": true, "UF_DEPARTMENT": departId, "ADMIN_MODE": true
        });

        for (let user of users) {
            contentHTML += templateUserBoxForSearch(user.ID, user.LAST_NAME, user.NAME, user.WORK_POSITION, user.USER_TYPE);
        }
        box.insertAdjacentHTML('beforeend', contentHTML);
    }

    // получение списка подразделений компаниии
    async getDepartments() {
        this.departments = await this.bx.callMethod("department.get");          // получение списка подразделений из Битрикс
        this.companyStructure = this.getTreeDepartments();                          // структура кмпании
    }

    // возвращает иерархическую структуру компании
    getTreeDepartments(parent=undefined) {
        let departmentsList = [];                                               // список департаментов с родительским подразделений = "parent"
        if (!this.departments) return;
        for (let department of this.departments) {
            if (department.PARENT === parent) {
                let children = this.getTreeDepartments(department.ID);          // список дочерних подразделений
                if (children.length !== 0) {
                    department.CHILDREN = children;
                }
                departmentsList.push(department);
            }
        }
        return departmentsList;
    }

    // вывод иерархической структуры подразделений предприятия
    renderDepartment() {
        this.boxDepartment.innerHTML = this.getHierarchHtmlDepartments(this.companyStructure);
    }

    // возвращает иерархическую HTML структуру подразделений на основе переданныхиерархических данных
    getHierarchHtmlDepartments(departments) {
        let contentHTML = '';
        for (let department of departments) {
            let departChildrenHTML = "";
            if (!department) return ""; 
            if (Array.isArray(department.CHILDREN) && department.CHILDREN.length >= 1) {
                departChildrenHTML += this.getHierarchHtmlDepartments(department.CHILDREN);
            }
            contentHTML += templateDepartContainerBox(department.ID, department.NAME, departChildrenHTML);
        }
        return contentHTML;
    }


    // <<<<<<<===== АНИМАЦИИ =====>>>>>>>
    animationOpen(element) {
        let anime = element.animate({
            height: `${element.scrollHeight}px`}, this.timeAnimate //* element.scrollHeight
        );
        anime.addEventListener('finish', function() {
            element.style.height = '100%';
        });
        this.animate = anime;
    }

    animationClose(element) {
        let height = element.offsetHeight || element.scrollHeight;
        element.style.height = `${height}px`;
        let anime = element.animate(
            {height: "0px"}, this.timeAnimate //* height
        )
        anime.addEventListener('finish', function() {
            element.style.height = '0px';
        });
        this.animate = anime;
    }


    // получить параметры филитрации для выполнения запроса
    getRequestParameters() {
        const selectedItems = this.field.getElementsByClassName("filter-item");
        let ids = [];
        for (let item of selectedItems) {
            ids.push(item.dataset.idBx);
        }
        return ids;

    }
}