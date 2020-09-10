function idCardValid(id) {
    const format = /^(([1][1-5])|([2][1-3])|([3][1-7])|([4][1-6])|([5][0-4])|([6][1-5])|([7][1])|([8][1-2]))\d{4}(([1][9]\d{2})|([2]\d{3}))(([0][1-9])|([1][0-2]))(([0][1-9])|([1-2][0-9])|([3][0-1]))\d{3}[0-9xX]$/;
    if (!format.test(id))
        return {'status': 0, 'msg': '身份证号码不合规'};
    const year = id.substr(6, 4),//身份证年
        month = id.substr(10, 2),//身份证月
        date = id.substr(12, 2),//身份证日
        time = Date.parse(month + '-' + date + '-' + year),
        now_time = Date.parse(new Date()),//当前时间戳
        dates = (new Date(year, month, 0)).getDate();
    if (time > now_time || date > dates)
        return {'status': -2, 'msg': '出生日期不合规'}

    const c = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2];   //系数
    const b = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2'];  //校验码对照表
    const id_array = id.split("");
    let sum = 0;
    for (let k = 0; k < 17; k++)
        sum += parseInt(id_array[k]) * parseInt(c[k]);
    if (id_array[17].toUpperCase() !== b[sum % 11].toUpperCase())
        return {'status': -1, 'msg': '身份证校验码不合规'}
    return {'status': 1, 'msg': '校验通过'}
}

function isHKCard(card) {
    // 港澳居民来往内地通行证
    // 规则： H/M + 10位或6位数字
    // 样本： H1234567890
    const reg = /^([A-Z]\d{6,10}(\(\w{1}\))?)$/;
    if (reg.test(card) === false) {
        return {'status': 0, 'msg': '港澳居民来往内地通行证号码不合规'};
    } else {
        return {'status': 1, 'msg': '校验通过'};
    }
}

function isTWCard(card) {
    // 台湾居民来往大陆通行证
    // 规则： 新版8位或18位数字， 旧版10位数字 + 英文字母
    // 样本： 12345678 或 1234567890B
    const reg = /^\d{8}|^[a-zA-Z0-9]{10}|^\d{18}$/;
    if (reg.test(card) === false) {
        return {'status': 0, 'msg': '台湾居民来往大陆通行证号码不合规'};
    } else {
        return {'status': 1, 'msg': '校验通过'};
    }
}

function isPassPortCard(card) {
    // 护照
    // 规则： 14/15开头 + 7位数字, G + 8位数字, P + 7位数字, S/D + 7或8位数字,等
    // 样本： 141234567, G12345678, P1234567
    const reg = /^([a-zA-z]|[0-9]){5,17}$/;
    if (reg.test(card) === false)
        return {'status': 0, 'msg': '护照号码不合规'};
    else
        return {'status': 1, 'msg': '校验通过'};
}

function checkForm() {
    const name = document.getElementById('stuName').value.replace(" ", "");

    if (name.length <= 0) {
        alert("请输入姓名");
        return false;
    }
    if (name.length > 20) {
        alert("请输入正确的姓名");
        return false;
    }

    const ID = document.getElementById('stuID').value.replace(" ", "");

    if (ID.length <= 0) {
        alert("请输入身份证信息");
        return false;
    }

    let state = idCardValid(ID)
    if (state.status === 1) return true;
    else if (state.status < 0) {
        alert(state.msg);
        return false;
    }

    state = isHKCard(ID)
    if (state.status === 1) return true;
    state = isTWCard(ID)
    if (state.status === 1) return true;
    state = isPassPortCard(ID)
    if (state.status === 1) return true;
    alert('请检查证件信息格式');
    return false;
}