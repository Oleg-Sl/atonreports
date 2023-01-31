// html-шаблон карточки компании из окна выбора
function templateCartCompanyElement(id_bx, name, inn) {
    return `
        <div class="filter-window-cart" data-id-bx="${id_bx}" data-inn="${inn}" data-name="${name}">
            <div class="filter-window-cart-name" title="${name}">${name}</div>
            <div class="filter-window-cart-inn"><b>ИНН:</b> ${inn}</div>
            <div class="filter-window-cart-id-bx"><b>ID в BX24:</b> ${id_bx}</div>
        </div>
    `;
}

// html-шаблон карточки направления сделки из окна выбора
function templateCartDirectionElement(id_bx, name) {
    return `
        <li class="list-group-item">
            <input class="form-check-input me-1" type="checkbox" data-id-bx="${id_bx}" value="${name}" aria-label="...">${name}
        </li>
    `;
}

// html-шаблон карточки направления сделки из окна выбора
function templateItemSingle(name) {
    return `
        <li class="" data-name="${name}">
            ${name}
        </li>
    `;
}

// html-шаблон элемента фильтра множественного выбора
function templateSelectItemElement(id_bx, name) {
    return `
        <div class="filter-item" data-id-bx="${id_bx}" data-name="${name}">
            <div class="filter-item-name" title="${name}">${name}</div>
            <div class="filter-item-delete"><button type="button" class="btn-close" aria-label="Close"></button></div>
        </div>
    `;
}


// Шаблоны окна "ПОИСК СОТРУДНИКА"


// Тип пользователя
const USER_TYPE = {
    "employee": "",
    "extranet": "Гость",
    "email": "Гость",
}


/**
 * Возвращает HTML-код шаблона сотрудника для контейнера - "поиск сотрудника по имени"/"поиск по подразделениям" 
 * @param {number} userId Идентификатор пользователя
 * @param {string} lastname Фамилия пользователя
 * @param {string} name Имя пользователя
 * @param {string} workposition Должность
 * @param {string} userType Тип пользователя
 * @returns {string} HTML код шаблона сотрудника
 */
function templateUserBoxForSearch(userId, lastname, name, workposition, userType) {
    let cssClassIntranet = "ui-selector-item-box-guest";    // css класс приглашенного пользователя
    // если пользователь экстранет
    if (userType === "employee") {
        cssClassIntranet = "";
    }
    return `
        <div class="ui-selector-item-box ui-selector-user-box ${cssClassIntranet}" data-user-id="${userId}" data-lastname="${lastname}" data-name="${name}" data-user-type="${userType}">
            <div class="ui-selector-item">
                <div class="ui-selector-item-useravatar"></div>
                <div class="ui-selector-item-titles">
                    <div class="ui-selector-item-supertitle"></div>
                    <div class="ui-selector-item-title-box">
                        <div class="ui-selector-item-title-box-title">${lastname} ${name}</div>
                        <div class="ui-selector-item-title-box-status"><span>${USER_TYPE[userType] || userType}</span></div>
                        <div class="ui-selector-item-title-box-workposition">${workposition}</div>
                    </div>
                    <div class="ui-selector-item-user-link">о сотруднике</div>
                </div>
                <div class="">
                    <div></div>
                </div>
            </div>
        </div>
    `;
}


/**
 * Возвращает HTML-код контейнера структуры компании
 * @param {number} departId Идентификатор подразделения
 * @param {string} departName Название подразделения
 * @param {string} departChildrenHTML HTML код дочерних подразделений
 * @returns {string} HTML код контейнера структуры компании
 */
function templateDepartContainerBox(departId, departName, departChildrenHTML) {
    return `
        <div class="ui-selector-item-box" data-depart-id="${departId}">
            <div class="ui-selector-item">
                <div class="ui-selector-item-avatar"><i class="bi bi-people-fill"></i></div>
                <div class="ui-selector-item-titles">
                    <div class="ui-selector-item-supertitle">Отдел</div>
                    <div class="ui-selector-item-title-box">${departName}</div>
                </div>
                <div class="ui-selector-item-indicator">
                    <div><i class="bi bi-chevron-down"></i></div>
                </div>
            </div>
            <div class="ui-selector-item-children">
                ${departChildrenHTML}
            </div>
        </div>
    `;
}


/**
 * Возвращает HTML-код шаблона сотрудника для контейнера - "выбранные пользователи"
 * @param {number} id Идентификатор пользователя
 * @param {string} lastname Фамилия пользователя
 * @param {string} name Имя пользователя
 * @param {string} usertype Тип пользователя
 * @returns {string} HTML код шаблона сотрудника
 */
function templateUserBoxForSelected(id, lastname, name, usertype) {
    let cssClassIntranet = "user-item-guest";          // css класс приглашенного пользователя
    // если пользователь экстранет
    if (usertype === "employee") {
        cssClassIntranet = "";
    }
    return `
        <div class="user-item ${cssClassIntranet}" data-user-id="${id}">
            <div class="user-item-content">
                <div class="user-item-avatar"></div>
                <div class="user-item-title">${lastname} ${name}</div>
            </div>
            <div class="user-item-remove">
                <div><button type="button" class="btn-close" aria-label="Close"></button></div>
            </div>
        </div>
    `;
}


/**
 * Возвращает HTML-код элемента для ввода значения поиска сотрудника - "выбранные пользователи"
 * @returns {string} HTML код строки поиска сотрудника
 */
function templateInputSearchUser() {
    return `
        <span>
            <input class="form-control form-control-sm search-user-input" type="text" autocomplete="on" placeholder="поиск" aria-label="default input example" id="">
        </span>
    `;
}



export {templateCartCompanyElement, templateCartDirectionElement, templateItemSingle, templateSelectItemElement, templateUserBoxForSearch, templateDepartContainerBox, templateUserBoxForSelected, templateInputSearchUser};

