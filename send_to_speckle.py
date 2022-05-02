import os
import c4d
import stl
from specklepy.api import operations
from specklepy.api.wrapper import StreamWrapper
from specklepy.objects.geometry import Mesh
from specklepy.logging.exceptions import SpeckleException

# the url to the stream or branch you want to send to (if not a branch url, it will default to the main branch)
STREAM_URL = "https://latest.speckle.dev/streams/0c6ad366c4/branches/c4d_tests"

# the file will get exported to an STL in this folder right next to your c4d file
STL_EXPORT_FOLDER_NAME = "stl_export"

# if you have a account on Speckle Manager, you don't need this
TOKEN = ""


def export_stl() -> str:
    """Export the current file to an STL in a subfolder next to this file's location"""
    active_doc = c4d.documents.GetActiveDocument()
    path = active_doc.GetDocumentPath()

    export_folder = os.path.join(path, STL_EXPORT_FOLDER_NAME)
    os.makedirs(export_folder, exist_ok=True)

    export_path = os.path.join(
        export_folder, f"{os.path.splitext(active_doc.GetDocumentName())[0]} EXPORT.stl"
    )

    saved = c4d.documents.SaveDocument(
        active_doc,
        export_path,
        saveflags=c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST,
        format=c4d.FORMAT_STL_EXPORT,
    )

    if not saved:
        raise SpeckleException("Failed to export file to STL")

    print(f"Exported STL to {export_path}")

    return export_path


def convert_stl(stl_file_path: str) -> Mesh:
    """
    Convert STL file into a Speckle Mesh
    (from the [speckle server import service](https://github.com/specklesystems/speckle-server/blob/main/packages/fileimport-service/stl/import_file.py))
    """
    # Parse input
    stl_mesh = stl.mesh.Mesh.from_file(stl_file_path)
    print(
        f"Parsed mesh with {stl_mesh.points.shape[0]} faces ({stl_mesh.points.shape[0] * 3} vertices)"
    )

    # Construct speckle obj
    vertices = stl_mesh.points.flatten().tolist()
    faces = []
    for i in range(stl_mesh.points.shape[0]):
        faces.extend([0, 3 * i, 3 * i + 1, 3 * i + 2])

    speckle_mesh = Mesh(
        vertices=vertices, faces=faces, colors=[], textureCoordinates=[]
    )
    print("Constructed Speckle Mesh object")

    return speckle_mesh


def send_to_speckle(
    wrapper: StreamWrapper, speckle_mesh: Mesh, commit_msg: str = None
) -> str:
    """Send the mesh to speckle and create a commit"""
    client = wrapper.get_client(TOKEN or None)

    if wrapper.branch_name and not client.branch.get(
        wrapper.stream_id, wrapper.branch_name
    ):
        client.branch.create(
            wrapper.stream_id,
            wrapper.branch_name,
            "File upload branch" if wrapper.branch_name == "uploads" else "",
        )

    obj_id = operations.send(base=speckle_mesh, transports=[wrapper.get_transport()])

    return client.commit.create(
        wrapper.stream_id,
        obj_id,
        wrapper.branch_name or "main",
        commit_msg or "STL file upload",
        source_application="cinema4D",
    )


def main() -> None:
    w = StreamWrapper(STREAM_URL)
    acct = w.get_account()
    if not acct.token or TOKEN:
        raise SpeckleException(
            "No token available. Please either add a Speckle Account to Speckle Manager or provide a token in `TOKEN`"
        )

    stl_path = export_stl()

    speckle_mesh = convert_stl(stl_path)

    commit_id = send_to_speckle(
        w, speckle_mesh, f"File upload: {os.path.basename(stl_path)}"
    )

    print(
        f"File uploaded to\n{w.server_url}/streams/{w.stream_id}/commits/{commit_id}\n"
    )


if __name__ == "__main__":
    main()
