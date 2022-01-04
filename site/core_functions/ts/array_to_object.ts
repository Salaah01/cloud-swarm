/**
 * Converts an array of objects into an object (dictionary like object).
 * @param {Array} array - Array to convert.
 * @param {String|Number} key - The key which will be become the key for each
 *  value. Must exist within each object within the array.
 */
export const array_to_object = (array: object[], key: string | number) => {
  return array.reduce((obj: any, item: any) => {
    obj[item[key]] = item;
    return obj;
  }, {});
};
