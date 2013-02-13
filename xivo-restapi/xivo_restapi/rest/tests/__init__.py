from mock import patch, Mock
from xivo_restapi.services.agent_management import AgentManagement
from xivo_restapi.services.campagne_management import CampagneManagement
from xivo_restapi.services.queue_management import QueueManagement
from xivo_restapi.services.recording_management import RecordingManagement

patcher_queue = patch("xivo_restapi.rest." + \
                             "API_queues.QueueManagement")
mock_queue = patcher_queue.start()
instance_queue_management = Mock(QueueManagement)
mock_queue.return_value = instance_queue_management

patcher_agent = patch("xivo_restapi.rest." + \
                             "API_agents.AgentManagement")
mock_agent = patcher_agent.start()
instance_agent_management = Mock(AgentManagement)
mock_agent.return_value = instance_agent_management

patcher_campaigns = patch("xivo_restapi.rest." + \
                             "API_campaigns.CampagneManagement")
mock_campaign = patcher_campaigns.start()
instance_campaign_management = Mock(CampagneManagement)
mock_campaign.return_value = instance_campaign_management

patcher_recordings = patch("xivo_restapi.rest." + \
                             "API_recordings.RecordingManagement")
mock_recording = patcher_recordings.start()
instance_recording_management = Mock(RecordingManagement)
mock_recording.return_value = instance_recording_management
