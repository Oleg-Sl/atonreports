export default class TableStatistic {
    constructor(table, loader, bx, createDeal) {
        this.table = table;
        this.bx = bx;
        this.createDeal = createDeal;

        // контейнер заголовка таблицы
        this.tableHeader = this.table.querySelector("thead");
        this.tableBody = this.table.querySelector("tbody");
        
        this.userCurrent = NaN;
        this.loader = loader;
        
    }

    async init(deltaDay, userCurrent, usersList) {
        this.userCurrent = userCurrent;
        this.usersList = usersList;
        this.dateTransitionDealToInactive = this.convertNumberOfDaysInDateObj(deltaDay);
        // обработчик перетаскивания таблицы по нажатию кнопки мыши
        this.handlerDragnDrop();
        // обработчик изменения ширины столбцов таблицы мышью
        this.handlerResizeWidthColumn();
        // инициализация обработчиков событий таблицы: вертикальны скролл страницы, горизантальный скролл таблицы
        this.initHandlerScroll();
        this.initHandler();

        // // обработчик событий наведения на пользователя или компанию
        // this.eventHoverElementsTable();

    }

    showTable() {
        this.table.classList.remove("d-none");
        this.loader.classList.add("d-none");
    }

    hideTable() {
        this.table.classList.add("d-none");
        this.loader.classList.remove("d-none");
    }

    initHandler() {
        // клик по компании или пользователю
        this.tableBody.addEventListener("click", async (e) => {
            let path = e.target.dataset.path;
            if (path) {
                await this.bx.openPath(path);
            }
        })
        // двойной клик на создание сделки
        this.tableBody.addEventListener('dblclick', async (e) => {
            const cellStatus = e.target.classList.contains("cell-add-deal");
            if (cellStatus) {
                let data = {};
                data.companyId = e.target.dataset.companyIdBx;
                data.categoryId = e.target.dataset.categoryIdBx;
                data.stageId = e.target.dataset.stageIdBx;
                data.directionCommaId = e.target.dataset.directionIdBx;
                data.responsibleId = this.userCurrent.ID;
                data.nameCompany = e.target.dataset.nameCompany;
                data.nameDirection = e.target.dataset.nameDirection;
                data.target1 = e.target;
                data.elementSumOWork = data.target1;

                const statusCellLeft = e.target.classList.contains("directory-column-border-left");
                if (statusCellLeft) {
                    // если клик по ячейкм сумма в работе
                    data.target2 = e.target.nextElementSibling;
                } else {
                    // если клик по ячейкм сумма успешных
                    data.target2 = e.target.previousElementSibling;
                    data.elementSumOWork = data.target2;
                }

                const status = e.target.dataset.allowed_add_deals;
                if (status === 0 || status === "0") {
                    let res = await this.createDeal.create(data);
                    console.log("Result create deal = ", res);
                    if (res) {
                        console.log("Result create deal = TRUE");
                        data['target1'].dataset.allowed_add_deals = 1;
                        data['target2'].dataset.allowed_add_deals = 1;
                        data['elementSumOWork'].innerHTML = "1";
                    }
                }
            }
        })
    }
    
    // инициализация событий таблицы: вертикальны скролл страницы, горизантальный скролл таблицы
    initHandlerScroll() {
        // обработчик вертикального скролла страницы - залипание первой строки таблицы
        document.addEventListener("scroll", (e) => requestAnimationFrame(() => {
            let elem = document.getElementsByTagName("table")[0];
            let offsetTop = $(document).scrollTop();
            if (elem.offsetTop < offsetTop) {
                $('th').css({
                    "top": offsetTop - elem.offsetTop
                })
            }
            else {
                $('th').css({"top": 0})
            }
        }))

        // обработчик горизантального скролла таблицы - залипание первого столбца таблицы
        this.table.addEventListener('scroll', (event)=>{
            let offsetLeft = this.table.scrollLeft;
            // console.log("offsetLeft => ", offsetLeft);
            $('.col-company').css({
                "left": offsetLeft
            })
        });
    }
    
    // обработчик перетаскивания таблицы по нажатию кнопки мыши
    handlerDragnDrop() {
        $("table").on("mousedown", function(event) {
            if (event.target.tagName == "SPAN" || event.target.tagName == "A" || event.which !== 1) {
                return;
            }
            let elem = document.getElementsByTagName("table")[0];
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
            $(document).on("mouseup",  function() {
                disabledDragDrop();
            });

            function disabledDragDrop() {
                // console.log("disabledDragDrop");
                document.removeEventListener('mousemove', onMouseMove);
                $("table").onmouseup = null;
                elemCursor.style.cursor = "default";
            };
    
        })
    }

    // обработчик изменения ширины столбцов таблицы - необходимо инициализировать после перерисовки таблицы
    handlerResizeWidthColumn() {
        // соответствие типу колонки ее ширины в "px" и "fr"
        const columnTypeToRatioMap = {
            'numeric-short': {  // столбцы - ИНН
                'min': 60,
                'max': 1
            },
            'numeric-medium': { 
                'min': 75,
                'max': 1.2
            },
            'numeric-long': { // столбцы - общ. сумма успешн. и в работе по компании 
                'min': 92,
                'max': 1.5
            },
            'text-short': { // столбцы - ДПК
                'min': 75,
                'max': 1
            },
            'text-long': {  // столбцы - компания, менеджер
                'min': 110,
                'max': 2.5
            }
        };
        
        const columns = [];
        let headerBeingResized;

        const onMouseMove = (e) => requestAnimationFrame(() => {
            if (e.which !== 1) {
                disabledResizeWidthColumn();
            }
            // console.log(">>> ", headerBeingResized);
            const horizontalScrollOffset = this.table.scrollLeft;
            // console.log("Смещение таблицы по оси X = ", horizontalScrollOffset);
            // console.log("Позиция курсора = ", e.clientX);
            // console.log("Текущее положение столбца = ", headerBeingResized.offsetLeft);
            const width = (horizontalScrollOffset + e.clientX) - headerBeingResized.offsetLeft;
            const column = columns.find(({ header }) => header === headerBeingResized);
            const min = column.minWidth

            // установить ширину столбца меньше минимального значения невозможно
            column.size = Math.max(min, width) + 'px';
            
            columns.forEach((column) => {
                if(column.size.startsWith('minmax')){
                    // console.log("column = ", column);
                    column.size = parseInt(column.header.clientWidth, 10) + 'px';
                    // console.log("column after = ", column);
                }
            });
            
            
            let sortPositionColumn = columns.map(({position}) => position).sort(compareNumeric);
            let sizeColumn = {};
            for (let col of columns) {
                sizeColumn[col.position] = col.size;
            }
            let arrSizeColumn = sortPositionColumn.map((ind) => sizeColumn[ind]);
            // console.log("arrSizeColumn = ", arrSizeColumn);
            this.table.style.gridTemplateColumns = arrSizeColumn.join(' ');
            localStorage.setItem('grid-template-columns', arrSizeColumn.join(' '));
        });

        const onMouseUp = () => {
            disabledResizeWidthColumn();
        };

        const disabledResizeWidthColumn = () => {
            window.removeEventListener('mousemove', onMouseMove);
            window.removeEventListener('mouseup', onMouseUp);
            headerBeingResized.classList.remove('header--being-resized');
            headerBeingResized = null;
        }

        const initResize = (event) => {
            // родительский блок ячейки таблицы в которой находится элемент "span" по которому произошло событие
            headerBeingResized = event.target.parentNode;
            window.addEventListener('mousemove', onMouseMove);
            window.addEventListener('mouseup', onMouseUp);
            headerBeingResized.classList.add('header--being-resized');
        };

        document.querySelectorAll('th').forEach((header) => {
            if (header.dataset.type && header.dataset.position) {
                const position = header.dataset.position;
                const min = columnTypeToRatioMap[header.dataset.type]['min'];
                const max = columnTypeToRatioMap[header.dataset.type]['max'];
                columns.push({
                    position,
                    minWidth: min,
                    header, 
                    size: `minmax(${min}px, ${max}fr)`,
                });
                header.querySelector('.resize-handle').addEventListener('mousedown', initResize);
            }
        });
    }

    renderTable(companySummary, directionSummary, companySummaryByDirection, companySummaryOpportunity) {
        this.companySummary = companySummary; 
        this.directionSummary = directionSummary;
        this.companySummaryByDirection = companySummaryByDirection;
        this.companySummaryOpportunity = companySummaryOpportunity;
        
        let contentHeadHTML = this.renderTableHeaderToHTML();
        this.tableHeader.innerHTML = contentHeadHTML;

        let contentBodyHTML = this.renderTableBodyToHTML();
        this.tableBody.innerHTML = contentBodyHTML;


        this.table.style.gridTemplateColumns = this.arrSizeColumn.join(' ');
        // this.showTable();
        this.handlerResizeWidthColumn();
    }

    // создание заголовка таблицы
    renderTableHeaderToHTML() {
        let directions = this.directionSummary;

        let startColumnWithDirData = 6;     // столбец с которого начинаются данные по направлениям
        let numberColumnsInDir = 2;         // столбцов данных в одном направлении
        // масссив с шириной колонок
        this.arrSizeColumn = ["minmax(150px, 2.5fr)", "minmax(120px, 1.5fr)", "minmax(100px, 1.5fr)", "minmax(95px, 1.2fr)", "minmax(95px, 1.2fr)"];
        
        let firstRowHTML = "";
        let secondRowHTML = "";
        let thirdRowHTML = `
            <th class="col-company header-count-active-deal" style="grid-column: $1/2;"></th>
            <th scope="col" colspan="${startColumnWithDirData}" class="header-count-active-deal" style="grid-column: 2/${startColumnWithDirData};">
                <div>Активные сделки</div>
            </th>
        `;

        for(let dirId in directions) {
            let dirName = directions[dirId].name;
            let numberActiveDealInDir = directions[dirId].count_active_deal;
            firstRowHTML += `
                <th scope="col" colspan="${numberColumnsInDir}" class="header-th-direction" style="grid-column: ${startColumnWithDirData}/${startColumnWithDirData + numberColumnsInDir}; grid-row: 1/2">
                    <div>${dirName}</div>
                    <span class="resize-handle"></span>
                </th>
            `;
            secondRowHTML += `
                <th scope="col" class="header-th-direction-data" data-type="numeric-medium" data-position="${startColumnWithDirData + 1}">Сумма в работе <span class="resize-handle"></span></th>
                <th scope="col" class="header-th-direction-data" data-type="numeric-medium" data-position="${startColumnWithDirData + 2}">Сумма успешных <span class="resize-handle"></span></th>
            `;
            thirdRowHTML += `
                <th scope="col" colspan="${numberColumnsInDir}" class="header-count-active-deal directory-column-border-left-border-left" style="grid-column: ${startColumnWithDirData}/${startColumnWithDirData + numberColumnsInDir};">
                    <div>${numberActiveDealInDir}</div>
                </th>
            `;

            startColumnWithDirData += numberColumnsInDir;

            this.arrSizeColumn.push("minmax(90px, 1.2fr)");
            this.arrSizeColumn.push("minmax(90px, 1.2fr)");
        }

        let contentHTML =`
            <tr class="text-center">
                <th scope="col" rowspan="2" class="col-company header-th-data header-th-sort-data" data-type="text-long" data-position="1">
                    Компания
                    <span class="resize-handle"></span>
                    <span class="sort-company-top">
                        <i data-order="name" class="bi bi-caret-up-fill sort-button" id="sorting-company-asc"></i>
                    </span>
                    <span class="sort-company-bottom">
                        <i data-order="-name" class="bi bi-caret-down-fill sort-button" id="sorting-company-desc"></i>
                    </span>
                </th>
                <th scope="col" rowspan="2" class="header-th-data header-th-sort-data" data-type="text-long"  data-position="3">
                    Менеджер 
                    <span class="resize-handle"></span>
                    <span class="sort-responsible-top">
                        <i data-order="responsible" class="bi bi-caret-up-fill sort-button" id="sorting-responsible-asc"></i>
                    </span>
                    <span class="sort-responsible-bottom">
                        <i data-order="-responsible" class="bi bi-caret-down-fill sort-button" id="sorting-responsible-asc"></i>
                    </span>
                </th>
                
                <th scope="col" rowspan="2" class="header-th-data header-th-sort-data" data-type="text-short"  data-position="4">
                    ДПК
                    <span class="resize-handle"></span>
                    <span class="sort-dpk-top">
                        <i data-order="dpk" class="bi bi-caret-up-fill sort-button" id="sorting-date_last_communication-asc"></i>
                    </span>
                    <span class="sort-dpk-bottom">
                        <i data-order="-dpk" class="bi bi-caret-down-fill sort-button" id="sorting-date_last_communication-asc"></i>
                    </span>
                </th>
                <th scope="col" rowspan="2" class="header-th-data header-th-sort-data" data-type="numeric-long" data-position="5">
                    Общая сумма в работе
                    <span class="resize-handle"></span>
                    <span class="sort-opportunity-work-top">
                        <i data-order="summa_by_company_work" class="bi bi-caret-up-fill sort-button"></i>
                    </span>
                    <span class="sort-opportunity-work-bottom">
                        <i data-order="-summa_by_company_work" class="bi bi-caret-down-fill sort-button"></i>
                    </span>
                </th>
                <th scope="col" rowspan="2" class="header-th-data header-th-sort-data" data-type="numeric-long" data-position="6">
                    Общая сумма успешных
                    <span class="resize-handle"></span>
                    <span class="sort-opportunity-sucсess-top">
                        <i data-order="summa_by_company_success" class="bi bi-caret-up-fill sort-button"></i>
                    </span>
                    <span class="sort-opportunity-sucсess-bottom">
                        <i data-order="-summa_by_company_success" class="bi bi-caret-down-fill sort-button"></i>
                    </span>
                </th>

                ${firstRowHTML}
            </tr>
            <tr class="text-center">
                ${secondRowHTML}
            </tr>
            <tr class="text-center">
                ${thirdRowHTML}
            </tr>
        `;
        return contentHTML       
    }

    // добавление данных в таблицу
    renderTableBodyToHTML() {
        let contentHTML = "";
        let companies = this.companySummary;
        console.log("companySummaryOpportunity = ", this.companySummaryOpportunity);
        for (let company of companies) {
            
            
            // let summaByCompanySuccess = company.summa_by_company_success || 0;
            // let summaByCompanyWork = company.summa_by_company_work || 0;
            let companyIdBx = company.id_bx;
            let companyName = company.name || "&ndash;";
            let companyInn = company.inn || "&ndash;";
            let companyResponsibleId = company.responsible || "&ndash;";
            let companyResponsibleTitle = this.getUserTitleByIBx(companyResponsibleId);
            let companyDpkDatetimeStr = company.dpk;
            let companyDpkDateStr = this.convertsDatetimeToString(companyDpkDatetimeStr);

            console.log("summaByCompanySuccess = ", this.companySummaryOpportunity[companyIdBx]);
            let summaByCompanySuccess = 0;
            let summaByCompanyWork = 0;
            if (this.companySummaryOpportunity[companyIdBx]) {
                summaByCompanySuccess = this.companySummaryOpportunity[companyIdBx].summa_by_company_success || 0;
                summaByCompanyWork = this.companySummaryOpportunity[companyIdBx].summa_by_company_work  || 0;
            }

            let dpkCellStyle = "";
            if (!companyDpkDatetimeStr || new Date(companyDpkDatetimeStr) < this.dateTransitionDealToInactive) {
                dpkCellStyle = "dpk-more-six-months";
            }

            let companyDirectionContent = this.renderTableBodyColDirToHTML(companyIdBx, companyName);

            contentHTML += `
                <tr>
                    <td class="col-company" data-name='${companyName}' data-inn='${companyInn}' data-id-bx='${companyIdBx}' >
                        <p><span class="col-href" data-path="/crm/company/details/${companyIdBx}/" title="${companyName.replace('"', '\'')}">${companyName}</span></p>
                    </td>
                    <td class="col-responsible" data-id-bx='${companyResponsibleId}'>
                        <p><span class="col-href" data-path="/company/personal/user/${companyResponsibleId}/" title="${companyResponsibleTitle}">${companyResponsibleTitle}</span></p>
                    </td>
                    <td class='${dpkCellStyle}'>${companyDpkDateStr || "&ndash;"}</td>
                    <td>${summaByCompanyWork.toLocaleString()}</td>
                    <td>${summaByCompanySuccess.toLocaleString()}</td>
                    ${companyDirectionContent}
                </tr>
            `;

        }
        return contentHTML;
    }

    // принимает список направлений компании и возвращает их HTML код для вставки в таблицу (столбцы с данными по направлениям)
    renderTableBodyColDirToHTML(companyIdBx, companyName) {
        let directions = this.directionSummary;
        let contentHTML = "";

        for (let dirIdBx in directions) {
            let valueCellAmountDealsInWork = "0";
            let styleCellAmountDealsInWork = "";
            let amountOfDealsInWork = "0";
            let amountOfSuccessfulDeals = "0";
            let isAllowedToCreateDeals = 0;
            let dirName = directions[dirIdBx].name;

            if (this.companySummaryByDirection[companyIdBx] && this.companySummaryByDirection[companyIdBx][dirIdBx]) {
                let companyDataByDir = this.companySummaryByDirection[companyIdBx][dirIdBx];
                amountOfDealsInWork = companyDataByDir.opportunity_work || "0";
                amountOfSuccessfulDeals = companyDataByDir.opportunity_success || "0";
                // если есть проваленные сделки
                if (companyDataByDir.actual_deal_failed) {
                    styleCellAmountDealsInWork = "cell-background-red";
                    valueCellAmountDealsInWork = "1";
                    isAllowedToCreateDeals = 1;
                }
                // если есть сделки на подготовке к работе
                if (companyDataByDir.actual_deal_preparation) {
                    styleCellAmountDealsInWork = "";
                    valueCellAmountDealsInWork = "1";
                    isAllowedToCreateDeals = 1;
                }
                // если есть сделки в работе
                if (companyDataByDir.actual_deal_work) {
                    styleCellAmountDealsInWork = "";
                    valueCellAmountDealsInWork = amountOfDealsInWork.toLocaleString();
                    isAllowedToCreateDeals = 1;
                }
            }
            
            contentHTML += `
                <td class='cell-add-deal directory-column-border-left ${styleCellAmountDealsInWork}' 
                    data-company-id-bx='${companyIdBx}' 
                    data-direction-id-bx='${dirIdBx}'
                    data-category-id-bx='43'
                    data-stage-id-bx='C43:NEW'
                    data-allowed_add_deals="${isAllowedToCreateDeals}"
                    data-name-company="${companyName.replace(/\"/g, '\'')}"
                    data-name-direction="${dirName.replace(/\"/g, '\'')}"
                >
                    ${valueCellAmountDealsInWork}
                </td>
                <td class='cell-add-deal'
                    data-company-id-bx='${companyIdBx}' 
                    data-direction-id-bx='${dirIdBx}'
                    data-category-id-bx='43'
                    data-stage-id-bx='C43:NEW'
                    data-allowed_add_deals="${isAllowedToCreateDeals}"
                    data-name-company="${companyName.replace(/\"/g, '\'')}"
                    data-name-direction="${dirName.replace(/\"/g, '\'')}"
                >
                    ${amountOfSuccessfulDeals.toLocaleString()}
                </td>
            `;
        }

        return contentHTML;
    }

    getUserTitleByIBx(userId) {
        let userObj = this.usersList[userId];
        if (userObj) {
            return `${this.usersList[userId].NAME || ""} ${this.usersList[userId].LAST_NAME || ""}`;
        }

        return id_bx;
    }

    convertNumberOfDaysInDateObj(numberDays) {
        let dateOffsetInMilliseconds = (24 * 60 * 60 * 1000) * numberDays;
        let actualDate = new Date();
        actualDate.setTime(actualDate.getTime() - dateOffsetInMilliseconds);
        return actualDate;
    }

    // принимает дату в формате ISO и возвращает дату в формате "дд.мм.гггг"
    convertsDatetimeToString(datetime) {
        if (!datetime) return;
        if (new Date(datetime) < new Date(2012, 1,1)) return;
        let date = new Date(datetime);
        let options = {
            year: 'numeric',
            month: 'numeric',
            day: 'numeric',
        };
        return date.toLocaleString("ru", options);
    }

    sortingSelection(orderName) {
        let sortButtons = this.tableHeader.querySelectorAll(".sort-button");
        sortButtons.forEach((elem) => {
            let order = elem.dataset.order;
            if (order === orderName) {
                elem.style.color = "#a996ff";
            } else {
                elem.style.color = "#fff";
            }
        })
    }


}

