/**
 * Generated by the protoc-gen-ts.  DO NOT EDIT!
 * compiler version: 3.21.12
 * source: bangumi/bangumi.proto
 * git: https://github.com/thesayyn/protoc-gen-ts */
import * as dependency_1 from "./../base/language_code";
import * as dependency_2 from "./../base/resources";
import * as dependency_3 from "./../base/external_meta";
import * as pb_1 from "google-protobuf";
export class Series extends pb_1.Message {
    #one_of_decls: number[][] = [];
    constructor(data?: any[] | {
        id?: number;
        bangumi_ids?: number[];
        external_metas?: dependency_3.ExternalMeta[];
    }) {
        super();
        pb_1.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [2, 3], this.#one_of_decls);
        if (!Array.isArray(data) && typeof data == "object") {
            if ("id" in data && data.id != undefined) {
                this.id = data.id;
            }
            if ("bangumi_ids" in data && data.bangumi_ids != undefined) {
                this.bangumi_ids = data.bangumi_ids;
            }
            if ("external_metas" in data && data.external_metas != undefined) {
                this.external_metas = data.external_metas;
            }
        }
    }
    get id() {
        return pb_1.Message.getFieldWithDefault(this, 1, 0) as number;
    }
    set id(value: number) {
        pb_1.Message.setField(this, 1, value);
    }
    get bangumi_ids() {
        return pb_1.Message.getFieldWithDefault(this, 2, []) as number[];
    }
    set bangumi_ids(value: number[]) {
        pb_1.Message.setField(this, 2, value);
    }
    get external_metas() {
        return pb_1.Message.getRepeatedWrapperField(this, dependency_3.ExternalMeta, 3) as dependency_3.ExternalMeta[];
    }
    set external_metas(value: dependency_3.ExternalMeta[]) {
        pb_1.Message.setRepeatedWrapperField(this, 3, value);
    }
    static fromObject(data: {
        id?: number;
        bangumi_ids?: number[];
        external_metas?: ReturnType<typeof dependency_3.ExternalMeta.prototype.toObject>[];
    }): Series {
        const message = new Series({});
        if (data.id != null) {
            message.id = data.id;
        }
        if (data.bangumi_ids != null) {
            message.bangumi_ids = data.bangumi_ids;
        }
        if (data.external_metas != null) {
            message.external_metas = data.external_metas.map(item => dependency_3.ExternalMeta.fromObject(item));
        }
        return message;
    }
    toObject() {
        const data: {
            id?: number;
            bangumi_ids?: number[];
            external_metas?: ReturnType<typeof dependency_3.ExternalMeta.prototype.toObject>[];
        } = {};
        if (this.id != null) {
            data.id = this.id;
        }
        if (this.bangumi_ids != null) {
            data.bangumi_ids = this.bangumi_ids;
        }
        if (this.external_metas != null) {
            data.external_metas = this.external_metas.map((item: dependency_3.ExternalMeta) => item.toObject());
        }
        return data;
    }
    serialize(): Uint8Array;
    serialize(w: pb_1.BinaryWriter): void;
    serialize(w?: pb_1.BinaryWriter): Uint8Array | void {
        const writer = w || new pb_1.BinaryWriter();
        if (this.id != 0)
            writer.writeUint64(1, this.id);
        if (this.bangumi_ids.length)
            writer.writePackedUint64(2, this.bangumi_ids);
        if (this.external_metas.length)
            writer.writeRepeatedMessage(3, this.external_metas, (item: dependency_3.ExternalMeta) => item.serialize(writer));
        if (!w)
            return writer.getResultBuffer();
    }
    static deserialize(bytes: Uint8Array | pb_1.BinaryReader): Series {
        const reader = bytes instanceof pb_1.BinaryReader ? bytes : new pb_1.BinaryReader(bytes), message = new Series();
        while (reader.nextField()) {
            if (reader.isEndGroup())
                break;
            switch (reader.getFieldNumber()) {
                case 1:
                    message.id = reader.readUint64();
                    break;
                case 2:
                    message.bangumi_ids = reader.readPackedUint64();
                    break;
                case 3:
                    reader.readMessage(message.external_metas, () => pb_1.Message.addToRepeatedWrapperField(message, 3, dependency_3.ExternalMeta.deserialize(reader), dependency_3.ExternalMeta));
                    break;
                default: reader.skipField();
            }
        }
        return message;
    }
    serializeBinary(): Uint8Array {
        return this.serialize();
    }
    static deserializeBinary(bytes: Uint8Array): Series {
        return Series.deserialize(bytes);
    }
}
export class Bangumi extends pb_1.Message {
    #one_of_decls: number[][] = [];
    constructor(data?: any[] | {
        id?: number;
        series_id?: number;
        names?: Name[];
    }) {
        super();
        pb_1.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [3], this.#one_of_decls);
        if (!Array.isArray(data) && typeof data == "object") {
            if ("id" in data && data.id != undefined) {
                this.id = data.id;
            }
            if ("series_id" in data && data.series_id != undefined) {
                this.series_id = data.series_id;
            }
            if ("names" in data && data.names != undefined) {
                this.names = data.names;
            }
        }
    }
    get id() {
        return pb_1.Message.getFieldWithDefault(this, 1, 0) as number;
    }
    set id(value: number) {
        pb_1.Message.setField(this, 1, value);
    }
    get series_id() {
        return pb_1.Message.getFieldWithDefault(this, 2, 0) as number;
    }
    set series_id(value: number) {
        pb_1.Message.setField(this, 2, value);
    }
    get names() {
        return pb_1.Message.getRepeatedWrapperField(this, Name, 3) as Name[];
    }
    set names(value: Name[]) {
        pb_1.Message.setRepeatedWrapperField(this, 3, value);
    }
    static fromObject(data: {
        id?: number;
        series_id?: number;
        names?: ReturnType<typeof Name.prototype.toObject>[];
    }): Bangumi {
        const message = new Bangumi({});
        if (data.id != null) {
            message.id = data.id;
        }
        if (data.series_id != null) {
            message.series_id = data.series_id;
        }
        if (data.names != null) {
            message.names = data.names.map(item => Name.fromObject(item));
        }
        return message;
    }
    toObject() {
        const data: {
            id?: number;
            series_id?: number;
            names?: ReturnType<typeof Name.prototype.toObject>[];
        } = {};
        if (this.id != null) {
            data.id = this.id;
        }
        if (this.series_id != null) {
            data.series_id = this.series_id;
        }
        if (this.names != null) {
            data.names = this.names.map((item: Name) => item.toObject());
        }
        return data;
    }
    serialize(): Uint8Array;
    serialize(w: pb_1.BinaryWriter): void;
    serialize(w?: pb_1.BinaryWriter): Uint8Array | void {
        const writer = w || new pb_1.BinaryWriter();
        if (this.id != 0)
            writer.writeUint64(1, this.id);
        if (this.series_id != 0)
            writer.writeUint64(2, this.series_id);
        if (this.names.length)
            writer.writeRepeatedMessage(3, this.names, (item: Name) => item.serialize(writer));
        if (!w)
            return writer.getResultBuffer();
    }
    static deserialize(bytes: Uint8Array | pb_1.BinaryReader): Bangumi {
        const reader = bytes instanceof pb_1.BinaryReader ? bytes : new pb_1.BinaryReader(bytes), message = new Bangumi();
        while (reader.nextField()) {
            if (reader.isEndGroup())
                break;
            switch (reader.getFieldNumber()) {
                case 1:
                    message.id = reader.readUint64();
                    break;
                case 2:
                    message.series_id = reader.readUint64();
                    break;
                case 3:
                    reader.readMessage(message.names, () => pb_1.Message.addToRepeatedWrapperField(message, 3, Name.deserialize(reader), Name));
                    break;
                default: reader.skipField();
            }
        }
        return message;
    }
    serializeBinary(): Uint8Array {
        return this.serialize();
    }
    static deserializeBinary(bytes: Uint8Array): Bangumi {
        return Bangumi.deserialize(bytes);
    }
}
export class BangumiIndex extends pb_1.Message {
    #one_of_decls: number[][] = [];
    constructor(data?: any[] | {
        index?: Bangumi[];
    }) {
        super();
        pb_1.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [1], this.#one_of_decls);
        if (!Array.isArray(data) && typeof data == "object") {
            if ("index" in data && data.index != undefined) {
                this.index = data.index;
            }
        }
    }
    get index() {
        return pb_1.Message.getRepeatedWrapperField(this, Bangumi, 1) as Bangumi[];
    }
    set index(value: Bangumi[]) {
        pb_1.Message.setRepeatedWrapperField(this, 1, value);
    }
    static fromObject(data: {
        index?: ReturnType<typeof Bangumi.prototype.toObject>[];
    }): BangumiIndex {
        const message = new BangumiIndex({});
        if (data.index != null) {
            message.index = data.index.map(item => Bangumi.fromObject(item));
        }
        return message;
    }
    toObject() {
        const data: {
            index?: ReturnType<typeof Bangumi.prototype.toObject>[];
        } = {};
        if (this.index != null) {
            data.index = this.index.map((item: Bangumi) => item.toObject());
        }
        return data;
    }
    serialize(): Uint8Array;
    serialize(w: pb_1.BinaryWriter): void;
    serialize(w?: pb_1.BinaryWriter): Uint8Array | void {
        const writer = w || new pb_1.BinaryWriter();
        if (this.index.length)
            writer.writeRepeatedMessage(1, this.index, (item: Bangumi) => item.serialize(writer));
        if (!w)
            return writer.getResultBuffer();
    }
    static deserialize(bytes: Uint8Array | pb_1.BinaryReader): BangumiIndex {
        const reader = bytes instanceof pb_1.BinaryReader ? bytes : new pb_1.BinaryReader(bytes), message = new BangumiIndex();
        while (reader.nextField()) {
            if (reader.isEndGroup())
                break;
            switch (reader.getFieldNumber()) {
                case 1:
                    reader.readMessage(message.index, () => pb_1.Message.addToRepeatedWrapperField(message, 1, Bangumi.deserialize(reader), Bangumi));
                    break;
                default: reader.skipField();
            }
        }
        return message;
    }
    serializeBinary(): Uint8Array {
        return this.serialize();
    }
    static deserializeBinary(bytes: Uint8Array): BangumiIndex {
        return BangumiIndex.deserialize(bytes);
    }
}
export class BangumiData extends pb_1.Message {
    #one_of_decls: number[][] = [];
    constructor(data?: any[] | {
        bangumi_id?: number;
        episodes?: Episode[];
        external_metas?: dependency_3.ExternalMeta[];
    }) {
        super();
        pb_1.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [2, 3], this.#one_of_decls);
        if (!Array.isArray(data) && typeof data == "object") {
            if ("bangumi_id" in data && data.bangumi_id != undefined) {
                this.bangumi_id = data.bangumi_id;
            }
            if ("episodes" in data && data.episodes != undefined) {
                this.episodes = data.episodes;
            }
            if ("external_metas" in data && data.external_metas != undefined) {
                this.external_metas = data.external_metas;
            }
        }
    }
    get bangumi_id() {
        return pb_1.Message.getFieldWithDefault(this, 1, 0) as number;
    }
    set bangumi_id(value: number) {
        pb_1.Message.setField(this, 1, value);
    }
    get episodes() {
        return pb_1.Message.getRepeatedWrapperField(this, Episode, 2) as Episode[];
    }
    set episodes(value: Episode[]) {
        pb_1.Message.setRepeatedWrapperField(this, 2, value);
    }
    get external_metas() {
        return pb_1.Message.getRepeatedWrapperField(this, dependency_3.ExternalMeta, 3) as dependency_3.ExternalMeta[];
    }
    set external_metas(value: dependency_3.ExternalMeta[]) {
        pb_1.Message.setRepeatedWrapperField(this, 3, value);
    }
    static fromObject(data: {
        bangumi_id?: number;
        episodes?: ReturnType<typeof Episode.prototype.toObject>[];
        external_metas?: ReturnType<typeof dependency_3.ExternalMeta.prototype.toObject>[];
    }): BangumiData {
        const message = new BangumiData({});
        if (data.bangumi_id != null) {
            message.bangumi_id = data.bangumi_id;
        }
        if (data.episodes != null) {
            message.episodes = data.episodes.map(item => Episode.fromObject(item));
        }
        if (data.external_metas != null) {
            message.external_metas = data.external_metas.map(item => dependency_3.ExternalMeta.fromObject(item));
        }
        return message;
    }
    toObject() {
        const data: {
            bangumi_id?: number;
            episodes?: ReturnType<typeof Episode.prototype.toObject>[];
            external_metas?: ReturnType<typeof dependency_3.ExternalMeta.prototype.toObject>[];
        } = {};
        if (this.bangumi_id != null) {
            data.bangumi_id = this.bangumi_id;
        }
        if (this.episodes != null) {
            data.episodes = this.episodes.map((item: Episode) => item.toObject());
        }
        if (this.external_metas != null) {
            data.external_metas = this.external_metas.map((item: dependency_3.ExternalMeta) => item.toObject());
        }
        return data;
    }
    serialize(): Uint8Array;
    serialize(w: pb_1.BinaryWriter): void;
    serialize(w?: pb_1.BinaryWriter): Uint8Array | void {
        const writer = w || new pb_1.BinaryWriter();
        if (this.bangumi_id != 0)
            writer.writeUint64(1, this.bangumi_id);
        if (this.episodes.length)
            writer.writeRepeatedMessage(2, this.episodes, (item: Episode) => item.serialize(writer));
        if (this.external_metas.length)
            writer.writeRepeatedMessage(3, this.external_metas, (item: dependency_3.ExternalMeta) => item.serialize(writer));
        if (!w)
            return writer.getResultBuffer();
    }
    static deserialize(bytes: Uint8Array | pb_1.BinaryReader): BangumiData {
        const reader = bytes instanceof pb_1.BinaryReader ? bytes : new pb_1.BinaryReader(bytes), message = new BangumiData();
        while (reader.nextField()) {
            if (reader.isEndGroup())
                break;
            switch (reader.getFieldNumber()) {
                case 1:
                    message.bangumi_id = reader.readUint64();
                    break;
                case 2:
                    reader.readMessage(message.episodes, () => pb_1.Message.addToRepeatedWrapperField(message, 2, Episode.deserialize(reader), Episode));
                    break;
                case 3:
                    reader.readMessage(message.external_metas, () => pb_1.Message.addToRepeatedWrapperField(message, 3, dependency_3.ExternalMeta.deserialize(reader), dependency_3.ExternalMeta));
                    break;
                default: reader.skipField();
            }
        }
        return message;
    }
    serializeBinary(): Uint8Array {
        return this.serialize();
    }
    static deserializeBinary(bytes: Uint8Array): BangumiData {
        return BangumiData.deserialize(bytes);
    }
}
export class Episode extends pb_1.Message {
    #one_of_decls: number[][] = [];
    constructor(data?: any[] | {
        index?: string;
        names?: Name[];
        resources?: dependency_2.ExternalResource[];
    }) {
        super();
        pb_1.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [2, 3], this.#one_of_decls);
        if (!Array.isArray(data) && typeof data == "object") {
            if ("index" in data && data.index != undefined) {
                this.index = data.index;
            }
            if ("names" in data && data.names != undefined) {
                this.names = data.names;
            }
            if ("resources" in data && data.resources != undefined) {
                this.resources = data.resources;
            }
        }
    }
    get index() {
        return pb_1.Message.getFieldWithDefault(this, 1, "") as string;
    }
    set index(value: string) {
        pb_1.Message.setField(this, 1, value);
    }
    get names() {
        return pb_1.Message.getRepeatedWrapperField(this, Name, 2) as Name[];
    }
    set names(value: Name[]) {
        pb_1.Message.setRepeatedWrapperField(this, 2, value);
    }
    get resources() {
        return pb_1.Message.getRepeatedWrapperField(this, dependency_2.ExternalResource, 3) as dependency_2.ExternalResource[];
    }
    set resources(value: dependency_2.ExternalResource[]) {
        pb_1.Message.setRepeatedWrapperField(this, 3, value);
    }
    static fromObject(data: {
        index?: string;
        names?: ReturnType<typeof Name.prototype.toObject>[];
        resources?: ReturnType<typeof dependency_2.ExternalResource.prototype.toObject>[];
    }): Episode {
        const message = new Episode({});
        if (data.index != null) {
            message.index = data.index;
        }
        if (data.names != null) {
            message.names = data.names.map(item => Name.fromObject(item));
        }
        if (data.resources != null) {
            message.resources = data.resources.map(item => dependency_2.ExternalResource.fromObject(item));
        }
        return message;
    }
    toObject() {
        const data: {
            index?: string;
            names?: ReturnType<typeof Name.prototype.toObject>[];
            resources?: ReturnType<typeof dependency_2.ExternalResource.prototype.toObject>[];
        } = {};
        if (this.index != null) {
            data.index = this.index;
        }
        if (this.names != null) {
            data.names = this.names.map((item: Name) => item.toObject());
        }
        if (this.resources != null) {
            data.resources = this.resources.map((item: dependency_2.ExternalResource) => item.toObject());
        }
        return data;
    }
    serialize(): Uint8Array;
    serialize(w: pb_1.BinaryWriter): void;
    serialize(w?: pb_1.BinaryWriter): Uint8Array | void {
        const writer = w || new pb_1.BinaryWriter();
        if (this.index.length)
            writer.writeString(1, this.index);
        if (this.names.length)
            writer.writeRepeatedMessage(2, this.names, (item: Name) => item.serialize(writer));
        if (this.resources.length)
            writer.writeRepeatedMessage(3, this.resources, (item: dependency_2.ExternalResource) => item.serialize(writer));
        if (!w)
            return writer.getResultBuffer();
    }
    static deserialize(bytes: Uint8Array | pb_1.BinaryReader): Episode {
        const reader = bytes instanceof pb_1.BinaryReader ? bytes : new pb_1.BinaryReader(bytes), message = new Episode();
        while (reader.nextField()) {
            if (reader.isEndGroup())
                break;
            switch (reader.getFieldNumber()) {
                case 1:
                    message.index = reader.readString();
                    break;
                case 2:
                    reader.readMessage(message.names, () => pb_1.Message.addToRepeatedWrapperField(message, 2, Name.deserialize(reader), Name));
                    break;
                case 3:
                    reader.readMessage(message.resources, () => pb_1.Message.addToRepeatedWrapperField(message, 3, dependency_2.ExternalResource.deserialize(reader), dependency_2.ExternalResource));
                    break;
                default: reader.skipField();
            }
        }
        return message;
    }
    serializeBinary(): Uint8Array {
        return this.serialize();
    }
    static deserializeBinary(bytes: Uint8Array): Episode {
        return Episode.deserialize(bytes);
    }
}
export class Name extends pb_1.Message {
    #one_of_decls: number[][] = [];
    constructor(data?: any[] | {
        language_code?: dependency_1.LanguageCode;
        name?: string;
    }) {
        super();
        pb_1.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
        if (!Array.isArray(data) && typeof data == "object") {
            if ("language_code" in data && data.language_code != undefined) {
                this.language_code = data.language_code;
            }
            if ("name" in data && data.name != undefined) {
                this.name = data.name;
            }
        }
    }
    get language_code() {
        return pb_1.Message.getFieldWithDefault(this, 1, dependency_1.LanguageCode.ENG) as dependency_1.LanguageCode;
    }
    set language_code(value: dependency_1.LanguageCode) {
        pb_1.Message.setField(this, 1, value);
    }
    get name() {
        return pb_1.Message.getFieldWithDefault(this, 2, "") as string;
    }
    set name(value: string) {
        pb_1.Message.setField(this, 2, value);
    }
    static fromObject(data: {
        language_code?: dependency_1.LanguageCode;
        name?: string;
    }): Name {
        const message = new Name({});
        if (data.language_code != null) {
            message.language_code = data.language_code;
        }
        if (data.name != null) {
            message.name = data.name;
        }
        return message;
    }
    toObject() {
        const data: {
            language_code?: dependency_1.LanguageCode;
            name?: string;
        } = {};
        if (this.language_code != null) {
            data.language_code = this.language_code;
        }
        if (this.name != null) {
            data.name = this.name;
        }
        return data;
    }
    serialize(): Uint8Array;
    serialize(w: pb_1.BinaryWriter): void;
    serialize(w?: pb_1.BinaryWriter): Uint8Array | void {
        const writer = w || new pb_1.BinaryWriter();
        if (this.language_code != dependency_1.LanguageCode.ENG)
            writer.writeEnum(1, this.language_code);
        if (this.name.length)
            writer.writeString(2, this.name);
        if (!w)
            return writer.getResultBuffer();
    }
    static deserialize(bytes: Uint8Array | pb_1.BinaryReader): Name {
        const reader = bytes instanceof pb_1.BinaryReader ? bytes : new pb_1.BinaryReader(bytes), message = new Name();
        while (reader.nextField()) {
            if (reader.isEndGroup())
                break;
            switch (reader.getFieldNumber()) {
                case 1:
                    message.language_code = reader.readEnum();
                    break;
                case 2:
                    message.name = reader.readString();
                    break;
                default: reader.skipField();
            }
        }
        return message;
    }
    serializeBinary(): Uint8Array {
        return this.serialize();
    }
    static deserializeBinary(bytes: Uint8Array): Name {
        return Name.deserialize(bytes);
    }
}
