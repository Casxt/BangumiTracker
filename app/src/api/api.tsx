import Axios from 'axios';
import { setupCache, buildWebStorage } from 'axios-cache-interceptor';
import { BangumiIndex, BangumiData } from '../proto/bangumi/bangumi';

const instance = Axios.create();
const cached_axios = setupCache(instance,
  {
    storage: buildWebStorage(localStorage, 'axios-cache:'),
    ttl: 1000 * 10 * 60,
  }
);

export const getBangumiIndex = () => {
  return cached_axios.get<BangumiIndex>('/storage/bangumi/index.json');
};

export const getBangumiData = (bangumi_index: number) => {
  return cached_axios.get<BangumiData>(`/storage/bangumi/${bangumi_index}/data.json`);
};

