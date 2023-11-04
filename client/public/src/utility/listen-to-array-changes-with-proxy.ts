// Note: This doesn't work if you modify the array in the callback. Keeping it here out of interest. :)
export function listenToArrayChangesWithProxy<T>(array: T[], callback: () => void) {
    // Source: https://stackoverflow.com/a/35610685
    const arrayChangeHandler: ProxyHandler<T[]> = {
        set: function(target, property, value, receiver): boolean {
            console.log('setting ' + property.toString() + ' for ' + target + ' with value ' + value);
            target[property as any] = value;
            // For example when using .push() we set the property "0"".
            // If we were to call .length property would be 'length'.
            if (typeof property === 'string' && !isNaN(parseInt(property as string))) {
                callback();
            }

            return true;
        },
    }

    return new Proxy<T[]>(array, arrayChangeHandler);
}