import {
    templateColMonthRowOne, 
    templateColMonthRowTwo, 
    templateColMonthRowTree, 
    templateColMonthRowFour, 
    templateThead,
    templateColMonthRowDepart,
    templateRowDepart,
    templateColMonthRowEmploye,
    templateRowEmploye,
} from './templates/template_table_by_month.js';


export default class TableByMonth {
    constructor(container, requests, infoData) {
        this.container = container;                                     // HTML-контейнер таблицы (тег - table)
        this.requests = requests;                                       // объект - выполнение запросов к серверу
        this.infoData = infoData;                                       // окно - просмотра дополнительных данных при клике по ячейке таблицы

        this.data = null;
        this.countWorking = null;
        this.duration = 20;
        this.summaryData = {};

        this.monthList = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];

        // инициализация событий таблицы
        this.initHandler();
        // инициализация события перетаскивания таблицы по левой кнопке мыши
        this.handlerDragnDrop();
        // фиксирование первой строки таблицы
        this.stickyFirstLine();
        
    }

    initHandler() {
        // обработчик горизантального скролла таблицы - залипание первого столбца таблицы
        this.container.addEventListener('scroll', (event)=>{
            let offsetLeft = event.target.scrollLeft;
            $('.table-by-month-first-column').css({
                "left": offsetLeft
            })
        });
    }

    // обновление данных таблицы
    render(data, summaryData, params) {
        // console.log("data = ", data);
        this.data = data;                                       // данные статистики
        this.summaryData = summaryData;                         // данные по звонкам за год
        this.year = params.actualYear;                          // год
        this.headDepart = params.headDepart;                    // руководители подразделений
        this.duration = params.duration;                        // минимальная длительность звонка

        // вывод данных и отрисовка таблицы
        this.renderTable();

        // смещение первого столбца - фиксация
        $('.table-by-month-first-column').css({
            "left": this.container.scrollLeft
        })
        
    }

    // отрисовка данных таблицы
    renderTable() {
        let contentHTML = "";
        let contentTbodyHTML = this.renderTbody();          // отрисовка тела таблицы
        let contentTheadHTML = this.renderThead();          // отрисовка заголовка таблицы
        contentHTML += contentTheadHTML;
        contentHTML += contentTbodyHTML;
        this.container.innerHTML = contentHTML;
    }
    
    // отрисовка заголовка таблицы
    renderThead() {
        let rowOne = `<th class="table-header table-by-month-first-column" colspan="1" rowspan="4"></th>`;
        let rowTwo = `<th class="table-header table-by-month-first-column" colspan="1" rowspan="4"></th>`;
        for (let numMonth in this.monthList) {
            let countCalls = this.getSummaryStatisticsForDepartment(this.data, numMonth, "data");
            // формирование HTML-строк заголовка таблицы
            rowOne += templateColMonthRowTwo(this.monthList[numMonth]);
            rowTwo += `<th class="table-header-two" colspan="4">${countCalls}</th>`;
        }
        rowOne += `<th class="table-header" colspan="1" rowspan="4">Итого</th>`;
        rowOne += `<th class="table-header" colspan="1" rowspan="4"></th>`;

        return `
            <thead>
                <tr>
                    ${rowOne}
                </tr>
                <tr>
                    ${rowTwo}
                </tr>
            </thead>
        `;
    }

    // отрисовка тела таблицы
    renderTbody() {
        if (!this.data) return;
        let contentHTML = "";
        for (let departmentData of this.data) {
            contentHTML += this.renderRowHeadDepart(departmentData);
            contentHTML += this.renderRowEmployeeDepart(departmentData);
        }

        return `
            <tbody>
                ${contentHTML}            
            </tbody>
        `;
    }

    // вывод строки руководителя подразделения
    renderRowHeadDepart(departmentData) {
        let contentHTML = "";
        let summaryCalls = 0;
        for (let numMonth in this.monthList) {
            let month = +numMonth + 1
            let countCalls = this.getSummaryStatisticsForDepartment(departmentData.data, month, "data");
            summaryCalls += countCalls;
            contentHTML += `
                <td data-month="${numMonth}">${countCalls}</td>
            `;
        }

        return `
            <tr class="head-department" data-depart-id="${departmentData.headId}">
                <td class="table-by-month-first-column">${departmentData.headLastname} ${departmentData.headName}</td>
                ${contentHTML}
                <td>${summaryCalls}</td>
            </tr>
        `;
    }

    // вывод списка сотрудников подразделения
    renderRowEmployeeDepart(departmentData) {
        let contentHTML = "";

        for (let user of departmentData.data) {
            let contentEmploeeHTML = "";
            // let summaryCalls = 0;
            for (let numMonth in this.monthList) {
                let month = +numMonth + 1
                let keyMonth = String(month);
                let countCalls = +user.data[keyMonth] || 0;
                // summaryCalls += countCalls;
                // HTML-код сотрудника
                contentEmploeeHTML += `
                    <td data-month="${numMonth}">${countCalls}</td>
                `;
            }
            contentHTML += `
                <tr data-depart-id="${departmentData.headId}" data-user-id="${user.ID}">
                    <td class="table-by-month-first-column">${user.LAST_NAME} ${user.NAME}</td>
                    ${contentEmploeeHTML}
                    <td>${this.summaryData[user.ID]}</td>
                </tr>
            `;
        }

        return contentHTML;  
    }

    getSummaryStatisticsForDepartment(data, month, key) {
        let keyMonth = String(month);
        let accum = 0;
        for (let user of data) {
            let count = user[key][keyMonth] || 0;
            accum += count;
        }
        return accum;
    }

    // возвращает сумму данных по подразделению за месяц
    getSummaryStatisticsForCompany(data, month, key) {
        let keyMonth = String(month);
        let accum = 0;
        for (let departmentData of data) {
            for (let user of departmentData.data) {
                let count = user[key][keyMonth] || 0;
                accum += count;
            }
        }
        return accum;
    }

    // обработчик перетаскивания таблицы по нажатию кнопки мыши
    handlerDragnDrop() {
        this.container.addEventListener("mousedown", (event) => {
            if (event.target.tagName == "A" || event.which !== 1) {
                return;
            }
            let elem = this.container;
            let elemCursor = document.getElementsByTagName("body")[0];
            elem.onselectstart = () => false;
            elemCursor.style.cursor = "grab";
            // стартовая позиция курсора на экране
            let cursorStart = {
                "X": event.pageX, 
                "Y": event.pageY
            }
            // координаты таблицы на странице
            let scrollStart = {
                "X": elem.scrollLeft,
                "Y": elem.scrollTop
            }
            // максимальное значение ScrolLeft
            let maxScrollWidth = elem.scrollWidth - elem.offsetWidth;
            // функция перемещения таблицы по горизонтали
            function onMouseMove(event) {
                if (event.which !== 1) {
                    disabledDragDrop();
                }
                let offset = scrollStart.X - event.pageX + cursorStart.X;
                if (offset < 0) {
                    offset = 0;
                }
                if (offset > maxScrollWidth) {
                    offset = maxScrollWidth;
                }
                elem.scrollLeft = offset;
            }
            // установка обработчика перемещения мыши
            document.addEventListener('mousemove', onMouseMove);
    
            // событие при отпускании кнопки мыши
            document.addEventListener("mouseup", (event) => {
                disabledDragDrop();
            })

            function disabledDragDrop() {
                document.removeEventListener('mousemove', onMouseMove);
                $("table").onmouseup = null;
                elemCursor.style.cursor = "default";
            };
    
        })
    }

    // фиксирование заголовка таблицы при вертикальной прокрутке
    stickyFirstLine() {
        requestAnimationFrame(tick);
        let table = this.container;
        function tick(timestamp) {
            // let elem = document.getElementsByTagName("table")[0];
            let offsetTop = $(document).scrollTop();
            if (table.offsetTop < offsetTop) {
                $('#tableStatisticMonth th').css({
                    "top": offsetTop - table.offsetTop
                })
            }
            else {
                $('#tableStatisticMonth th').css({"top": 0})
            }

            requestAnimationFrame(tick);
        }
    }

    // преобразование объекта даты в строку формата: гггг-мм-дд
    toDateStringMy(date) {
        let year = date.getFullYear();
        let month = date.getMonth();
        let day = date.getDate();
        return `${year}-${+month + 1}-${day}`;
    }
}

function toFixedTwoSimbol(numb) {
    if (+numb < 10) {
        return "0" + numb
    }
    return numb;
}



