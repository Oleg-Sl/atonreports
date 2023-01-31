

export default class CreateDeal {
    constructor(bx24) {
        this.bx24 = bx24;
    }

    async create(data) {
        let companyId = data.companyId;
        let categoryId = data.categoryId;
        let stageId = data.stageId;
        let directionCommaId = data.directionCommaId;
        let responsibleId = data.responsibleId;
        
        let nameCompany = data.nameCompany;
        let nameDirection = data.nameDirection;

        let isCreateDeal = confirm(`Создать сделку в компании \"${nameCompany}\" по направлению \"${nameDirection}\"?`);
        if (!isCreateDeal) return;

        console.log("Создание сделки");
        // создание сделки в BX24
        let dealId = await this.creatDeal(companyId, categoryId, stageId, directionCommaId, responsibleId);
        console.log(`Создана сделка с ID = ${dealId}`);
        if (!dealId) {
            console.error(`Не удалось создать сделку для компании - ${companyId}, направления - ${directionCommaId}`);
            return;
        }
        console.log(`Получение контактов компании`);
        // получение контактов компании
        let contactsList = await this.getCompanyContactsList(companyId);
        console.log(`Контакты компании: ${JSON.stringify(contactsList)}`);
        
        if (Array.isArray(contactsList) && contactsList.length != 0) {
            console.log(`Добавление контактов к компании ${dealId}`);
            // добавленеи контактов к сделке
            let resultAddContacts = await this.addContactsToDeal(dealId, contactsList);
            console.log(`Контакты компании получены`);
        }
        console.log(`Открытие сделки ${dealId} во вкладке`);
        // открытие сделки во вкладке
        let res = await this.openDeal(dealId);
        console.log(`Вкладка сделки открыта = ${JSON.stringify(res)}`);
        return true;
    }

    // получение контактов компании
    async getCompanyContactsList(companyId) {
        let contacts = await this.bx24.callMethod(
            'crm.company.contact.items.get',
            {id: companyId},
        )
        return contacts;
    }

    // создание сделки в BX24
    async creatDeal(companyId, categoryId, stageId, directionCommaId, responsibleId) {
        let dealId = await this.bx24.callMethod(
            'crm.deal.add',
            {
                fields: { 
                    COMPANY_ID: companyId,
                    CATEGORY_ID: categoryId,
                    STAGE_ID: stageId,
                    UF_CRM_1610523951: directionCommaId,
                    ASSIGNED_BY_ID: responsibleId,
                    OPENED: "Y",
                },
                params: { REGISTER_SONET_EVENT: "Y" }
            }
        );
        return dealId;
    }

    // добавленеи контактов к сделке
    async addContactsToDeal(dealId, contacts) {
        let response = await this.bx24.callMethod(
            'crm.deal.contact.items.set',
            {
                id: dealId,
                items: contacts
            }
        )
        console.log(`Результат добавления контактов к компании: ${JSON.stringify(response)}`);
        if (response) return true;
    }

    // открытие сделки во вкладке
    async openDeal(dealId) {
        await this.bx24.openPath(`/crm/deal/details/${dealId}/`);
    }
}


