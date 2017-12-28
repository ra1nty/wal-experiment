'lang sweet.js';

export syntax open = function(ctx){
    let url = ctx.next().value;
    //ctx.expand('Expression');
    let result =  #``;
    result = result.concat(#`await__page.open(${url});`);
    return result;
};

export syntax fill = function(ctx){
    let selector = ctx.next().value;
    let val = ctx.next().value;
    let result = #``;
    result = result.concat(#`
        await__page.invokeMethod(
            'evaluate', 
            function(a1,a2) {
                document.querySelector(a1).value = a2;
            },
            ${selector},
            ${val}
        );
    `);
    return result;
}

export syntax click = function(ctx){
    let selector = ctx.next().value;
    let result = #``;
    result = result.concat(#`
        await__page.invokeMethod(
            'evaluate', 
            function(a1) {
                document.querySelector(a1).click();
            },
            ${selector}
        );
    `);
    return result;
}

export syntax find = function(ctx){
    let selector = ctx.next().value;
    let result = #``;
    result = result.concat(#`
        await__page.invokeMethod(
            'evaluate', 
            function(a1) {
                return parseInt(document.querySelector(a1).innerText);
            },
            ${selector}
        )
    `);
    return result;
}