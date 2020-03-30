import moment from 'moment';

const snakeToCamel = (s: string) => s.replace(
  /([-_][a-z])/g,
  (group) => group.toUpperCase()
    .replace('-', '')
    .replace('_', ''));

const keysToCamel = (o: any): any => {
  if (o instanceof Object) {
    const n: any = {};

    Object.keys(o).forEach((k) => {
      n[snakeToCamel(k)] = keysToCamel(o[k]);
    });
    return n;

  } else if (o instanceof Array) {
    return o.map((i) => {
      return keysToCamel(i);
    });
  }

  return o;
};

const extractDate = (dateString: string) => {
  return moment(dateString).format('YYYY/MM/DD');
};

export { snakeToCamel, keysToCamel, extractDate };
