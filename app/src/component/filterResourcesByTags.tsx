import { ExternalResource } from "../proto/base/resources";



export function filterResourcesByTags(resource: ExternalResource, selectedTags?: Set<string>): boolean {
    if (resource.share_dmhy_org) {
        const dmhy_data = resource.share_dmhy_org;
        const tags = dmhy_data.tags;
        if (selectedTags && selectedTags.size > 0) {
            if (tags) {
                let counter = 0;
                for (let i = 0; i < tags.length && counter < selectedTags.size; i++) {
                    if (selectedTags.has(tags[i].tag)) {
                        counter++;
                    }
                }
                return counter === selectedTags.size;
            }
            return false;
        }
        return true;
    }
    return false;
}
