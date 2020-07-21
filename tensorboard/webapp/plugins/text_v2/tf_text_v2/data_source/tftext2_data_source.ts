/* Copyright 2020 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';

import {TextRunListing} from '../store/text_types';
import {TBHttpClient} from '../../../../webapp_data_source/tb_http_client';

/** @typehack */ import * as _typeHackRxjs from 'rxjs';

export abstract class Tftext2DataSource {
  abstract fetchRuns(): Observable<TextRunListing>;
}
@Injectable()
export class Tftext2HttpServerDataSource implements Tftext2DataSource {
  private readonly httpPathPrefix = 'data/plugin/text-v2';

  constructor(private http: TBHttpClient) {}

  fetchRuns() {
    return this.http.get<TextRunListing>(this.httpPathPrefix + '/runs');
  }
}
