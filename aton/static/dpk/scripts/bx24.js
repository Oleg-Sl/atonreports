
export default  class BX {
    constructor() {

    }

    async callMethod(method, params = {}) {
        return new Promise((resolve, reject) => {
            let callback = result => {
                if (result.status != 200 || result.error()) {
                    console.log(`${result.error()} (callMethod ${method}: ${JSON.stringify(params)})`);
                    return reject("");
                }
                return resolve(result.data());
            };
            BX24.callMethod(method, params, callback);
        });
    }

    // async callBatch(method, params = {}) {
    //     return new Promise((resolve, reject) => {
    //         let callback = result => {
    //             if (result.status != 200 || result.error()) {
    //                 console.log(`${result.error()} (callMethod ${method}: ${JSON.stringify(params)})`);
    //                 return reject("");
    //             }
    //             return resolve(result.data());
    //         };
    //         BX24.callBatch(method, params, callback);
    //     });
    // }

    // Открыть путь внутри портала
    async openPath(path) {
        return new Promise((resolve, reject) => {
            let callback = result => {
                // if (result.status != 200 || result.error()) {
                //     // console.log(`${result}`);
                //     return reject("");
                // }
                // return resolve(result.data());
                return resolve();
            };
            BX24.openPath(path, callback);
        });
    }

    // Получить начтройки приложения по ключу
    async getSettingsAppByKey(key) {
        let value = await BX24.appOption.get(key);
        return value;
    }

    // Установка настройки приложения: ключ-значение
    async setSettingsAppByKey(key, value) {
        return new Promise((resolve, reject) => {
            let callback = result => {
                if (result.status != 200 || result.error()) {
                    console.log(`${result.error()} (callMethod ${method}: ${JSON.stringify(params)})`);
                    return reject("");
                }
                return resolve(result.data());
            };
            BX24.appOption.set(key, value, callback);
        });
    }

    // Выполнение пакетного запроса
    async batchMethod(reqPackage) {
        return new Promise((resolve, reject) => {
            let callback = result => {
                let response = {};
                for (let key in result) {
                    if (result[key].status != 200 || result[key].error()) {
                        console.log(`${result[key].error()} (method ${reqPackage[key]["method"]}: ${JSON.stringify(reqPackage[key]["params"])})`);
                        // return reject("");
                        continue;
                    }
                    let resData = result[key].data();
                    response[key] = resData;
                }
                return resolve(response);
            };
            BX24.callBatch(reqPackage, callback);
        });
    }

    async callMethodForLong(method, params = {}) {
        return new Promise((resolve, reject) => {
            let callback = result => {
                if (result.status != 200 || result.error()) {
                    console.log(`${result.error()} (callMethod ${method}: ${JSON.stringify(params)})`);
                    return reject("");
                }
                return resolve(result.answer);
            };
            BX24.callMethod(method, params, callback);
        });
    }

    // Выполнение длинного пакетного запроса
    async longBatchMethod(method, params) {
        let response = await this.callMethodForLong(method, params);
        let result = response.result;               // данные
        let next = response.next;                   // следующий номер элемента для извлечения
        let total = response.total;                 // всего элементов
        if (next) {
            let requestsList = this.generatingRequests(method, params, next, total);        // формирование списка запросов
            let batchList = this.splittingListRequests(requestsList);                       // разбитие списка запросов на "пачки"
            let countBatch = batchList.length;      // общее количество BATCH запросов
            let count = 0;                          // количество выпоненных BATCH запросов
            for (let batch of batchList) {
                let res = await this.batchMethod(batch);                                    //
                // result = result.concat(...res);
                for (let key in res) {
                    result = result.concat(res[key]);
                }
                count++;
                console.log(`Выполнено ${count} запросов из ${countBatch}`);
            }
        }
        
        return result;
    }


     // формирование списка запросов для batch
     generatingRequests(method, params, start, total) {
        let batch = [];                                     // список запросов
        for (let ind=start; ind < total; ind += 50) {
            let paramsStart = JSON.parse(JSON.stringify(params));
            paramsStart.start = ind;
            // формирование запроса
            let req = {
                method,
                params: paramsStart
            };
            batch.push(req);
        }    
        return batch;
    }

    // формирование списка пакетов запросов batch 
    splittingListRequests(requestsList){
        let requestsBatch = [];                     // 
        let batch = {};                             // пакет batch запросов
        let count = 1;                              // текущее количество запросов в пакете batch запросов
        for (let ind in requestsList) {
            if (count > this.batchLength) {         // если количество запросов в пакете превысило лимит
                requestsBatch.push(batch);          // добавление пакета batch запросов 
                batch = {};
                count = 1
            }
            batch[ind] = requestsList[ind];         // добавление запроса в пакет batch
            count++;                                // кол-во запросов в пакете batch
        }
        requestsBatch.push(batch);                  // добавление пакета batch запросов 
        
        return requestsBatch;
    }

}


