from .dataframes import AnchorDataFrame

# TODO: Enum for measurement types ?

class AnchoringMesh(object):

    @classmethod
    def from_api(cls, filters={}):
        mesh = cls()
        mesh.anchors = AnchorDataFrame.from_api(filters)
        return mesh
        # TODO: Add methods/df to see anchoring mesh stats (number of nodes, ...)
        # TODO: Add method for generating overlay

    # A towards B
    def __fetch_results(self, fqdn_a, fqdn_b, af, t, filters):
        anchors = AnchorDataFrame.from_api(filters)
        anchor_a = anchors[anchors.fqdn == fqdn_a].iloc[0]
        anchor_b = anchors[anchors.fqdn == fqdn_b].iloc[0]
        mesh_measurements_b = anchor_b.fetch_mesh_measurements()
        msm_to_b = mesh_measurements_b[(mesh_measurements_b.af == af) &
                                       (mesh_measurements_b.type == t)].iloc[0]
        return msm_to_b.fetch_results({
            **filters, 'probe_ids': anchor_a.probe
        }).loc[anchor_a.probe]

    # A towards B
    def fetch_results_single(self, fqdn_a, fqdn_b, af, t, filters={}):
        """Fetch results for the mesh measurements from `fqdn_a` to `fqdn_b`.

        Args:
            fqdn_a (str): Fully qualified domain name of the source anchor.
            fqdn_b (str): Fully qualified domain name of the target anchor.
            af (int): IP version (4 or 6).
            t (str): Measurement type (ping, traceroute, ...).
            filters (dict): TODO: https://atlas.ripe.net/docs/api/v2/reference/#!/measurements.

        Returns:
            MeasurementResultDataFrame
        """
        res_ab = self.__fetch_results(fqdn_a, fqdn_b, af, t, filters)
        return res_ab

    # A towards B, and B towards A
    def fetch_results_pair(self, fqdn_a, fqdn_b, af, t, filters={}):
        """Fetch results for the mesh measurements from `fqdn_a` to `fqdn_b` and from `fqdn_b` to `fqdn_a`.

        Args:
            fqdn_a (str): Fully qualified domain name of the first anchor..
            fqdn_b (str): Fully qualified domain name of the second anchor.
            af (int): IP version (4 or 6).
            t (str): Measurement type (ping, traceroute, ...).
            filters (dict): TODO: https://atlas.ripe.net/docs/api/v2/reference/#!/measurements.

        Returns:
            (MeasurementResultDataFrame, MeasurementResultDataFrame)
        """
        res_ab = self.__fetch_results(fqdn_a, fqdn_b, af, t, filters)
        res_ba = self.__fetch_results(fqdn_b, fqdn_a, af, t, filters)
        return res_ab, res_ba

    # # All towards B, and B towards all
    # def fetch_results_all_pairs(self, fqdn_b, af, t, filters={}):
    #     pass

    # All towards B
    # def fetch_results(fqdn_a, fqdn_b)
