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
    render(data, params) {
        console.log("data = ", data);
        this.data = data;                                       // данные статистики
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
        contentHTML += this.renderThead();          // отрисовка заголовка таблицы
        // contentHTML += this.renderTbody();          // отрисовка тела таблицы
        // contentHTML += this.renderTfooter();        // отрисовка футера таблицы
        this.container.innerHTML = contentHTML;
    }
    
    // отрисовка заголовка таблицы
    renderThead() {
        let rowOne = `<th class="table-header table-by-month-first-column" colspan="1" rowspan="4"></th>`;
        for (let numMonth in this.monthList) {
            // формирование HTML-строк заголовка таблицы
            rowOne += templateColMonthRowTwo(this.monthList[numMonth]);
        }
        rowOne = `<th class="table-header" colspan="1" rowspan="4">Итого</th>`;

        return templateThead(rowOne);
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
        for (let numMonth in this.monthList) {
            let month = +numMonth + 1
            // количество встреч департамента в месяц
            let countMeeting = this.getSummaryStatisticsForDepartment(departmentData.data, month, "meetings_fact");
            // количество звонков департамента в месяц
            let countCalls   = this.getSummaryStatisticsForDepartment(departmentData.data, month, "calls_fact");
            // среднее количество звонков департамента в день за месяц
            let countCallsAvg = Math.ceil(countCalls / this.getCountWorkingDays(month)) || 0;
            // план звонков по подразделению в день на месяц
            let countCallsPlan = this.getSummaryStatisticsForDepartment(departmentData.data, month, "calls_plan");

            let actualDate = new Date();
            let date = new Date(this.year, numMonth, 1);

            let cssMarker = "";
            if (+countCallsPlan > +countCallsAvg && actualDate > date) {
                cssMarker = "marker-display";
            }

            contentHTML += templateColMonthRowDepart(countMeeting, countCalls, countCallsAvg, countCallsPlan, cssMarker, month);
        }

        // Фамилия + Имя руководителя подразделения
        let headDepart = `${departmentData.headLastname} ${departmentData.headName}`;
        return templateRowDepart(contentHTML, headDepart);
    }

    // вывод списка сотрудников подразделения
    renderRowEmployeeDepart(departmentData) {
        let contentHTML = "";
        let actualDate = new Date();

        for (let user of departmentData.data) {
            let contentEmploeeHTML = "";
            for (let numMonth in this.monthList) {
                // let cssClassCell = "";
                let month = +numMonth + 1
                let keyMonth = String(month);

                let date = new Date(this.year, numMonth, 1);

                // фактическое кол-во встреч
                let countMeeting = +user.meetings_fact[keyMonth] || 0;
                // фактическое кол-во звонков
                let countCalls = +user.calls_fact[keyMonth] || 0;
                // среднее кол-во звонков в день
                let countCallsAvg = Math.ceil(countCalls / this.getCountWorkingDays(month));
                // план по звонкам в день
                let countCallsPlan = user.calls_plan[keyMonth];
                // количество комментариев за месяц
                let countComments = +user.comments[keyMonth] || 0;
                
                // рарешение на редактирование плана по звонкам
                let edit = this.verificationEditTable(numMonth)

                let dateStart = new Date(this.year, numMonth, 1);
                let dateEnd = new Date(this.year, +numMonth + 1, 0);
                
                let params = {
                    countMeeting, 
                    countCalls, 
                    countCallsAvg, 
                    countCallsPlan, 
                    countComments, 
                    edit, 
                    month, 
                    dateStart: this.toDateStringMy(dateStart), 
                    dateEnd: this.toDateStringMy(dateEnd),
                    user: user.ID,
                    departId: departmentData.headId,
                }

                // HTML-код сотрудника
                contentEmploeeHTML += templateColMonthRowEmploye(params);

                this.summaryData[keyMonth]["meeting"] += countMeeting;
                this.summaryData[keyMonth]["calls"] += +countCalls;
                this.summaryData[keyMonth]["calls_avg"] += countCallsAvg;
                this.summaryData[keyMonth]["calls_plan"] += +countCallsPlan || 0;
            }

            let userTitle = `${user.LAST_NAME} ${user.NAME}`;
            contentHTML += templateRowEmploye(contentEmploeeHTML, departmentData.headId, user.ID, userTitle)
        }

        return contentHTML;  
    }

    // вывод итога таблицы
    renderTfooter() {
        let contentHTML = "";
        let actualDate = new Date();

        for (let numMonth in this.monthList) {
            let keyMonth = String(+numMonth + 1);
            let date = new Date(this.year, numMonth, 1);
            let ccount_avg = "&ndash;";
            if (actualDate > date) {
                ccount_avg = this.summaryData[keyMonth]["calls_avg"];
                // ccount_avg = Math.ceil(this.summaryData[keyMonth]["calls"] / +numMonth + 1);
            }

            contentHTML += `
                <td class="table_by-month-border-left">${this.summaryData[keyMonth]["meeting"]}</td>
                <td>${this.summaryData[keyMonth]["calls"]}</td>
                <td>${this.summaryData[keyMonth]["calls_avg"]}</td>
                <td>${this.summaryData[keyMonth]["calls_plan"]}</td>
            `;
        }

        return `
            <tr class="footer-departments">
                <td class="table-by-month-first-column">Итого</td>
                ${contentHTML}
            </tr>
        `;
    }

    // возвращает сумму данных по подразделению за месяц
    getSummaryStatisticsForDepartment(data, month, key) {
        let keyMonth = String(month);
        let accum = 0;
        for (let user of data) {
            let count = user[key][keyMonth] || 0;
            accum += count;
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



