import CustomCard from '@components/Card'
import { Button, Card, CardBody, CardFooter, CardHeader, Dropdown, DropdownItem, DropdownMenu, DropdownTrigger } from '@heroui/react'
import { More01Icon, More02Icon } from 'hugeicons-react'
import { ArrowRight, BeakerIcon, Brush, Calendar, CheckCircleIcon, CircleAlert, CircleCheck, Clock, ClockIcon, Cog, Ellipsis, Plus, User } from 'lucide-react'
import React from 'react'
import { useNavigate } from 'react-router-dom'

export const projects = [
    {
        "id": 1,
        "project_name": "API Gateway Sync",
        "description": "Establishes real-time data sync via API Gateway",
        "created_by": "Astrid",
        "created_date": "2024-11-15",
        "status": "In Progress",
        "priority": "Normal",
        "last_updated": "2025-05-01",
        "tech_stack": ["Mulesoft", "Java", "REST API"],
        "integration_type": "Microservices"
    },
    {
        "id": 2,
        "project_name": "Legacy Connector Hub",
        "description": "Connects legacy ERP systems with Mulesoft APIs",
        "created_by": "DevOps Team",
        "created_date": "2024-09-20",
        "status": "Completed",
        "priority": "Medium",
        "last_updated": "2025-03-18",
        "tech_stack": ["SAP", "Mulesoft", "Oracle DB"],
        "integration_type": "ERP"
    },
    {
        "id": 3,
        "project_name": "Enterprise Data Flow",
        "description": "Automates data flow between microservices",
        "created_by": "Priya Sharma",
        "created_date": "2025-01-10",
        "status": "In Progress",
        "priority": "Normal",
        "last_updated": "2025-04-25",
        "tech_stack": ["Node.js", "Kafka", "Mulesoft"],
        "integration_type": "Data Streaming"
    },
    {
        "id": 4,
        "project_name": "Customer Insights API",
        "description": "Gathers customer analytics across platforms",
        "created_by": "Rahul Verma",
        "created_date": "2025-02-05",
        "status": "Development",
        "priority": "Medium",
        "last_updated": "2025-04-10",
        "tech_stack": ["Python", "Mulesoft", "MongoDB"],
        "integration_type": "Analytics"
    },
    {
        "id": 5,
        "project_name": "Inventory Sync Pro",
        "description": "Ensures seamless inventory updates across systems",
        "created_by": "Sarah Gupta",
        "created_date": "2025-03-21",
        "status": "Testing",
        "priority": "Normal",
        "last_updated": "2025-04-30",
        "tech_stack": ["Mulesoft", "PostgreSQL", "AWS"],
        "integration_type": "Inventory Management"
    },
    {
        "id": 6,
        "project_name": "Payment Gateway Integration",
        "description": "Enables secure payment processing across multiple platforms",
        "created_by": "Finance Team",
        "created_date": "2025-04-01",
        "status": "Planning",
        "priority": "Critical",
        "last_updated": "2025-05-10",
        "tech_stack": ["Mulesoft", "Stripe API", "JavaScript"],
        "integration_type": "Payment Processing"
    },
    {
        "id": 7,
        "project_name": "HR Workflow Automation",
        "description": "Streamlines HR tasks like payroll, leave requests, and onboarding",
        "created_by": "HR Team",
        "created_date": "2025-02-15",
        "status": "Development",
        "priority": "Medium",
        "last_updated": "2025-05-05",
        "tech_stack": ["Mulesoft", "Workday API", "Python"],
        "integration_type": "HR System"
    },
    {
        "id": 8,
        "project_name": "IoT Device Manager",
        "description": "Integrates IoT sensors with enterprise analytics",
        "created_by": "IoT Team",
        "created_date": "2025-03-05",
        "status": "Design Phase",
        "priority": "Normal",
        "last_updated": "2025-04-28",
        "tech_stack": ["Mulesoft", "AWS IoT", "Node.js"],
        "integration_type": "IoT & Cloud"
    }
];

function List() {
    const navigate = useNavigate()
    const StatusIcon = ({ status }) => {
        return status === "Completed" ? (
            <CircleCheck className="h-5 w-5 text-green-500 mr-2" />
        ) : status === "In Progress" ? (
            <Clock className="h-5 w-5 text-yellow-500 mr-2" />
        ) : status === "Development" ? (
            <Cog className="h-5 w-5 text-blue-500 mr-2" />
        ) : status === "Design Phase" ? (
            <Brush className="h-5 w-5 text-red-500 mr-2" />
        ) : (
            <BeakerIcon className="h-5 w-5 text-purple-500 mr-2" />
        );
    }

    const PriorityIcon = ({ priority }) => {
        return priority === "Critical" ? (
            <CircleAlert className="h-5 w-5 text-red-500 mr-2" />
        ) : priority === "Medium" ? (
            <CircleAlert className="h-5 w-5 text-yellow-500 mr-2" />
        ) : (
            <CircleCheck className="h-5 w-5 text-green-500 mr-2" />
        );
    }
    const ProjectCard = ({ project }) => {
        return (
            <Card
                classNames={{
                    header: 'px-5',
                    body: 'px-5',
                    footer: 'px-5'
                }}
                radius='sm'
            >
                <CardHeader className='flex justify-between items-center border-b-1'>
                    <div className="font-semibold text-lg">{project.project_name}</div>
                    <Dropdown>
                        <DropdownTrigger>
                            <Button isIconOnly size='sm' variant='light'><Ellipsis /></Button>
                        </DropdownTrigger>
                        <DropdownMenu aria-label="Action event example" onAction={(key) => alert(key)}>
                            <DropdownItem key="edit">Edit</DropdownItem>
                            <DropdownItem key="delete" className="text-danger" color="danger">
                                Delete
                            </DropdownItem>
                        </DropdownMenu>
                    </Dropdown>
                </CardHeader>
                <CardBody className='flex flex-cols gap-1'>
                    <p className="text-default-600 mb-3">{project.description}</p>

                    <p>⚙️ Tech Stack: {project.tech_stack.join(", ")}</p>
                    <p>🔌 Integration Type: <span className="">{project.integration_type}</span></p>

                    {/* <p className='text-default-600 flex items-center gap-1'>
                        <User size={18} />
                        Created By: {project.created_by}
                    </p>
                    <p className='text-default-600 flex items-center gap-1'>
                        <Calendar size={18} />
                        Created Date: {project.created_date}
                    </p> */}

                    <div className="flex items-center mt-2">
                        <StatusIcon status={project.status} />
                        <span className="font-medium">{project.status}</span>
                    </div>


                    {/* <div className="flex items-center mt-2">
                        {project.status === "Completed" ? (
                            <CheckCircleIcon className="h-5 w-5 text-green-500 mr-2" />
                        ) : (
                            <ClockIcon className="h-5 w-5 text-yellow-500 mr-2" />
                        )}
                        <span className="font-medium">{project.status}</span>
                    </div> */}

                </CardBody>
                <CardFooter className='border-t-1 py-2 flex justify-between'>
                    <div className='text-sm text-default-500'>
                        Created on {project.created_date} by {project.created_by}
                    </div>
                    <Button onPress={() => navigate(`/projects/${project.id}`)}>Select <ArrowRight size={16} /></Button>
                </CardFooter>
            </Card>
        )
    }

    return (
        <>
            <div className="flex justify-between mb-5">
                <div>
                    <h1 className="text-3xl font-bold text-gray-800 mb-1">
                        Projects
                    </h1>
                    <p className="text-gray-600">
                        List of available projects
                    </p>
                </div>
                <div>
                    <Button color='primary'><Plus size={16} /> Create new Project</Button>
                </div>
            </div>

            <div className="grid grid-cols-2 gap-6">

                {projects.map((project, index) => (
                    <ProjectCard key={index} project={project} />
                ))}
            </div>
        </>
    )
}

export default List