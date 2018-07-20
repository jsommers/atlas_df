from .dataframes import AnchorDataFrame


class AnchoringMesh(object):
    def __init__(self):
        self.anchors = AnchorDataFrame()
        # TODO: Add methods/df to see anchoring mesh stats (number of nodes, ...)
        # TODO: Add method for generating overlay

    # A towards b
    def __fetch_results(self, fqdn_a, fqdn_b, af, t, filters):
        anchor_a = self.anchors[self.anchors.fqdn == fqdn_a].iloc[0]
        anchor_b = self.anchors[self.anchors.fqdn == fqdn_b].iloc[0]
        mesh_measurements_b = anchor_b.fetch_mesh_measurements()
        msm_to_b = mesh_measurements_b[(mesh_measurements_b.af == af) &
                                       (mesh_measurements_b.type == t)].iloc[0]
        return msm_to_b.fetch_results({
            **filters, 'probe_ids': anchor_a.probe
        }).loc[anchor_a.probe]

    def fetch_results(self, fqdn_a, fqdn_b, af, t, filters={}):
        res_ab = self.__fetch_results(fqdn_a, fqdn_b, af, t, filters)
        res_ba = self.__fetch_results(fqdn_b, fqdn_a, af, t, filters)
        return res_ab, res_ba
