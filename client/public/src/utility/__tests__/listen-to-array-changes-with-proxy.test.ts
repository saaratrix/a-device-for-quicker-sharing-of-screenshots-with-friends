import { listenToArrayChangesWithProxy } from "../listen-to-array-changes-with-proxy";

describe('listen to array changes with proxy tests', () => {

  // ## This doesn't work because modifying the array in the callback bugs .length.
  // it ('should allow editing in callback', () => {
  //   let callbacks = 0;
  //   const items = listenToArrayChangesWithProxy<string>([], function () {
  //     items.splice(0, 1);
  //     callbacks++;
  //   });
  //
  //   items.push('test');
  //   expect(items.length).toBe(0);
  //   expect(callbacks).toBe(1);
  // });

  it('should handle multiple instances independently', () => {
    const instance1 = new TestClass();
    const instance2 = new TestClass();

    // Modify the first instance
    instance1.items[0] = 'instance1-item';
    expect(instance1.items.length).toBe(1);
    expect(instance1.callbacksInvoked).toBe(1);

    expect(instance2.callbacksInvoked).toBe(0);
    expect(instance2.items.length).toBe(0);

    instance2.items.push('instance2-item');
    expect(instance1.items.length).toBe(1);
    expect(instance1.callbacksInvoked).toBe(1);

    expect(instance2.items.length).toBe(1);
    expect(instance2.callbacksInvoked).toBe(1);

    instance1.items.push('instance1-item2');
    instance1.items.splice(0, 1);

    expect(instance1.items.length).toBe(1);
    expect(instance1.callbacksInvoked).toBe(3);
    expect(instance1.items[0]).toBe('instance1-item2');

    expect(instance2.items.length).toBe(1);
    expect(instance2.callbacksInvoked).toBe(1);
    expect(instance2.items[0]).toBe('instance2-item');
  });

  class TestClass {
    readonly items = listenToArrayChangesWithProxy<string>([], () => {
      this.callbacksInvoked++;
    });

    callbacksInvoked = 0;
  }

});