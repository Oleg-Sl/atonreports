let DOMAIN = "https://otchet.atonlab.ru/dpk/api/v1";
let URL__CREATE_UPDATE_COMPANY = `${DOMAIN}/create-update-company/`;
let URL__CREATE_UPDATE_DEAL = `${DOMAIN}/create-update-deal/`;
let URL__CREATE_UPDATE_CALLS = `${DOMAIN}/create-update-calls/`;


async function callMethod(method, params = {}) {
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

async function addHandler() {
    await callMethod(
        'event.bind',
        {
			"event": "ONCRMCOMPANYADD",
			"handler": URL__CREATE_UPDATE_COMPANY,
		},
		console.log('Обработчик ONCRMCOMPANYADD установлен')
    )
    await callMethod(
        'event.bind',
        {
			"event": "ONCRMCOMPANYUPDATE",
			"handler": URL__CREATE_UPDATE_COMPANY,
		},
		console.log('Обработчик ONCRMCOMPANYUPDATE установлен')
    )
    await callMethod(
        'event.bind',
        {
			"event": "ONCRMCOMPANYDELETE",
			"handler": URL__CREATE_UPDATE_COMPANY,
		},
		console.log('Обработчик ONCRMCOMPANYDELETE установлен')
    )
    await callMethod(
        'event.bind',
        {
			"event": "ONCRMDEALADD",
			"handler": URL__CREATE_UPDATE_DEAL,
		},
		console.log('Обработчик ONCRMDEALADD установлен')
    )
    await callMethod(
        'event.bind',
        {
			"event": "ONCRMDEALUPDATE",
			"handler": URL__CREATE_UPDATE_DEAL,
		},
		console.log('Обработчик ONCRMDEALUPDATE установлен')
    )
    await callMethod(
        'event.bind',
        {
			"event": "ONCRMDEALDELETE",
			"handler": URL__CREATE_UPDATE_DEAL,
		},
		console.log('Обработчик ONCRMDEALDELETE установлен')
    )
    await callMethod(
        'event.bind',
        {
			"event": "ONVOXIMPLANTCALLEND",
			"handler": URL__CREATE_UPDATE_CALLS,
		},
		console.log('Обработчик ONVOXIMPLANTCALLEND установлен')
    )

}

async function removeHandler() {
    await callMethod(
        'event.unbind',
        {
			"event": "ONCRMCOMPANYADD",
			"handler": URL__CREATE_UPDATE_COMPANY,
		},
		console.log('Обработчик ONCRMCOMPANYADD удален')
    )
    await callMethod(
        'event.unbind',
        {
			"event": "ONCRMCOMPANYUPDATE",
			"handler": URL__CREATE_UPDATE_COMPANY,
		},
		console.log('Обработчик ONCRMCOMPANYUPDATE удален')
    )
    await callMethod(
        'event.unbind',
        {
			"event": "ONCRMCOMPANYDELETE",
			"handler": URL__CREATE_UPDATE_COMPANY,
		},
		console.log('Обработчик ONCRMCOMPANYDELETE удален')
    )
    await callMethod(
        'event.unbind',
        {
			"event": "ONCRMDEALADD",
			"handler": URL__CREATE_UPDATE_DEAL,
		},
		console.log('Обработчик ONCRMDEALADD удален')
    )
    await callMethod(
        'event.unbind',
        {
			"event": "ONCRMDEALUPDATE",
			"handler": URL__CREATE_UPDATE_DEAL,
		},
		console.log('Обработчик ONCRMDEALUPDATE удален')
    )
    await callMethod(
        'event.unbind',
        {
			"event": "ONCRMDEALDELETE",
			"handler": URL__CREATE_UPDATE_DEAL,
		},
		console.log('Обработчик ONCRMDEALDELETE удален')
    )
    await callMethod(
        'event.unbind',
        {
			"event": "ONVOXIMPLANTCALLEND",
			"handler": URL__CREATE_UPDATE_CALLS,
		},
		console.log('Обработчик ONVOXIMPLANTCALLEND удален')
    )

}


BX24.init(async function(){
    await removeHandler();
    await addHandler();

    BX24.installFinish();
});

